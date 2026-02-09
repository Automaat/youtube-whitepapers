Generate 11 presentation slides based on the podcast about "On the Criteria to Be Used in Decomposing Systems into Modules" by David Parnas (1972).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: The Revolutionary Paper That Changed Software Design
- David Parnas's 1972 paper introduced modular programming principles that still guide software architecture today
- Despite being over 50 years old, its insights remain remarkably relevant for modern systems
- Challenged conventional thinking about how to decompose systems into modules
- Introduced "information hiding" as the fundamental criterion for modular decomposition
- Used the KWIC (Keyword in Context) indexing system as a practical demonstration

## Slide 2: Two Contrasting Approaches to System Decomposition
- Traditional approach: divide system by processing steps or functional flowchart
- Each module corresponds to one stage in the data processing pipeline
- Parnas's approach: divide by design decisions and potential changes
- Each module hides one design decision behind a stable interface
- Key insight: modules should encapsulate decisions that are likely to change
- The second approach creates more maintainable and flexible systems

## Slide 3: The KWIC System Example
- KWIC: Keyword In Context - a system for creating permuted indexes
- Takes input lines and generates circular shifts sorted alphabetically
- Example: "Design Patterns" generates "Design Patterns" and "Patterns Design"
- Traditional decomposition: Input → Circular Shift → Alphabetizer → Output
- Each module knows internal data structures of others
- Changes to data representation require modifying multiple modules

## Slide 4: Problems with Traditional Functional Decomposition
- Modules are tightly coupled through shared data structures
- Every module needs to understand implementation details of others
- Changing data representation requires modifying multiple modules
- Teams cannot work independently on different modules
- System becomes rigid and difficult to maintain
- Early design decisions become frozen in the architecture

## Slide 5: Information Hiding - The Core Principle
- Each module becomes a "black box" hiding one design decision
- Module's interface shields other modules from its internal implementation
- Examples of hidden decisions: data storage format, algorithms, hardware specifics
- Modules communicate only through well-defined interfaces
- Changes to hidden decisions don't ripple through the system
- Teams can work in parallel without knowing each other's implementation details

## Slide 6: Parnas's Modular Decomposition of KWIC
- Line Storage module: hides how lines are stored (memory, file, compressed)
- Input module: hides the input format and parsing logic
- Circular Shifter module: hides how shifts are generated and stored
- Alphabetizer module: hides the sorting algorithm
- Output module: hides the output format and presentation
- Master Control: coordinates module interactions without knowing their internals

## Slide 7: Benefits of Information Hiding
- Independent development: teams work in parallel without coordination
- Changeability: modifications stay localized within single modules
- Comprehensibility: understand one module without knowing others' internals
- Reusability: modules with clean interfaces can be reused in other systems
- Testing: modules can be tested independently through their interfaces
- Performance optimization: can replace implementations without affecting system

## Slide 8: Creating Natural Hierarchies
- Information hiding naturally creates layered architectures
- Lower-level modules hide hardware and platform specifics
- Higher-level modules hide business logic and algorithms
- Each layer depends only on layers below, not above
- Similar to modern concepts: device drivers → OS → applications
- Enables portability and platform independence

## Slide 9: Modern Applications of Parnas's Principles
- Object-oriented programming: classes hide internal state behind methods
- Abstract data types: separate interface from implementation
- Microservices: each service hides its database and technology stack
- Docker containers: hide application dependencies and runtime environment
- API design: REST/GraphQL interfaces hide backend implementation
- Cloud services: hide infrastructure complexity behind service interfaces

## Slide 10: Design Process Based on Information Hiding
- Don't decompose by workflow steps or functional diagram
- Identify your system's biggest design secrets and uncertainties
- List decisions likely to change: algorithms, data formats, external services
- Encapsulate each changeable decision in its own module
- Define minimal, stable interfaces that hide these decisions
- Create modules that can evolve independently without breaking others

## Slide 11: Question for You
What secrets should we be hiding in today's distributed cloud systems that leverage AI models and serve millions of users - is it the cloud provider, language model choice, scaling approach, or do 21st-century problems require entirely new decomposition criteria?