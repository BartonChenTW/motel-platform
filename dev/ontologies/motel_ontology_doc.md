MOTEL Project: Energy Technology & Process Ontology Documentation

updated date: 2026-05-29

This document provides a comprehensive overview of the MOTEL Project Energy Technology and Process Ontology Schema, formulated in Turtle (TTL) format using the Web Ontology Language (OWL).

The ontology acts as a formal TBox (Terminological Schema) designed to classify physical infrastructure, thermodynamic conversion operations, and energy carriers. It provides a structured blueprint that can be systematically populated with specific asset data (ABox) derived from project technology sheets.

1. Architectural Philosophy: The "Noun vs. Verb" Paradigm

The most critical architectural decision in this ontology is the strict separation between Technology and Process. This decoupling solves common challenges in energy system modelling (such as representing multi-output systems or multi-mode storage).

Technology (The "Noun" / Hardware)

Definition: A physical, tangible asset, machine, or facility built or installed on-site.

Core Class: motel:Technology

Characteristics: Tangible assets that hold physical or financial parameters (e.g., capital costs, lifespan, geographic coordinates, nominal capacity).

Examples: motel:GasTurbine, motel:FuelCell, motel:BatteryUnit.

Process (The "Verb" / Operational Action)

Definition: A physical, chemical, or thermodynamic conversion or storage sequence taking place within a technology.

Core Class: motel:Process

Characteristics: Intangible operations that govern thermodynamic behavior (e.g., process efficiency, input/output energy carrier relationships).

Examples: motel:ElectricityGenerationProcess, motel:HydrogenProductionProcess.

Rationale & Power of the Split

By separating these two layers, the ontology cleanly models complex multi-mode technologies without creating redundant classes:

Combined Heat and Power (CHP): Instead of creating a physical CombinedHeatPowerTechnology class, a physical asset (such as motel:FuelCell or motel:GasTurbine) is simply asserted to execute the dual-output process motel:CombinedHeatPowerGenerationProcess. This represents CHP as an operational profile rather than a separate machine.

Pumped Hydro Storage: A single motel:HydropowerPlant asset can be asserted to execute motel:ElectricityGenerationProcess (turbining) in one state, and motel:EnergyStorageProcess (pumping) in another.

2. Structural Class Hierarchy

The schema is organized into four main structural classes, all stemming from the top-level class motel:MOTELEntity.

motel:MOTELEntity
 ├── motel:Technology (The Hardware)
 │    ├── motel:ConversionTechnology
 │    │    ├── motel:ElectricityGenerationTechnology (GasTurbine, FuelCell, PhotovoltaicSystem, etc.)
 │    │    ├── motel:ThermalGenerationTechnology (HeatPumpUnit, BoilerSystem)
 │    │    ├── motel:ChemicalSynthesisTechnology (ElectrolyserUnit, GasifierUnit, FischerTropschUnit)
 │    │    ├── motel:CarbonCaptureTechnology
 │    │    └── motel:TransmissionInfrastructure (ElectricalGridNode, DistrictHeatingNetworkNode)
 │    └── motel:StorageTechnology
 │         ├── motel:ElectrochemicalStorage (BatteryUnit)
 │         ├── motel:MechanicalStorage (ReservoirUnit)
 │         └── motel:ThermalStorage (ThermalStorageTank)
 ├── motel:Process (The Operation)
 │    ├── motel:CarbonCaptureProcess
 │    ├── motel:ElectricityGenerationProcess ──┐
 │    │                                        ├─► motel:CombinedHeatPowerGenerationProcess
 │    ├── motel:HeatGenerationProcess ─────────┘
 │    ├── motel:HydrogenProductionProcess
 │    ├── motel:HydrocarbonSynthesisProcess
 │    └── motel:EnergyStorageProcess
 └── motel:EnergyCarrier (The Fuel/Medium)
      └── (Electricity, Hydrogen, Methane, Ammonia, CO2, Biomass, Heat)


3. RDF Properties

The ontology utilizes custom Object and Datatype properties to construct semantic triples.

Object Properties (Entity-to-Entity Relationships)

motel:executesProcess

Domain: motel:Technology

Range: motel:Process

Description: Links a physical asset to the thermodynamic or operational actions it is capable of performing.

motel:hasEnergyCarrierIn

Domain: motel:Technology OR motel:Process (defined via owl:unionOf)

Range: motel:EnergyCarrier

Description: Declares the required fuel, medium, or feedstocks.

motel:hasEnergyCarrierOut

Domain: motel:Technology OR motel:Process

Range: motel:EnergyCarrier

Description: Declares the resulting outputs or products.

Datatype Properties (Entity-to-Literal Relationships)

motel:techID (xsd:string): Unique alphanumeric identifier corresponding to engineering spreadsheets (e.g., "T_C_Conv_Solar_PV").

motel:unitOperationName (xsd:string): Common engineering term for the physical system (e.g., "Anode Recirculation Fuel Cell").

4. Open Energy Ontology (OEO) Alignment

To promote interoperability within the broader energy system research community, the schema includes the oeo: prefix (https://openenergyplatform.org/ontology/oeo/).

Individual instances generated using this schema are intended to be multi-typed. For example, when instantiating a specific solar project:

motel:My_Solar_PV_Asset a motel:PhotovoltaicSystem , oeo:SolarPV .


This multi-typing preserves MOTEL-specific properties while allowing global semantic search queries to identify the asset as an OEO-compliant solar PV system.