Generate 11 presentation slides based on the podcast about Borg, Omega, and Kubernetes.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Google's Container Orchestration Evolution

- Borg: Google's first-generation cluster manager (2003-2004)
- Omega: Second-generation system addressing Borg's architectural limitations
- Kubernetes: Open-source third generation building on lessons learned
- All three systems manage containerized workloads across thousands of machines
- Evolution driven by need for better scalability, flexibility, and developer experience

## Slide 2: Borg Architecture and Challenges

- Monolithic centralized architecture with single master controlling all scheduling
- Teams began creating custom wrappers around Borg API for their specific needs
- Tight coupling between components made system difficult to evolve
- Configuration validation and consistency scattered across multiple layers
- Success at scale revealed fundamental architectural constraints

## Slide 3: Omega's Shared State Design

- Replaced monolithic scheduler with multiple independent schedulers
- API enforces validation, consistency checks, and admission control centrally
- Shared state store using Paxos consensus for coordination
- Each scheduler can have domain-specific logic and priorities
- Optimistic concurrency control resolves conflicts when they occur

## Slide 4: Managing Configuration Updates at Scale

- Configuration updates in Borg required careful coordination to avoid conflicts
- Omega's shared state allows multiple controllers to operate independently
- Version control and conflict resolution built into the core API
- Enables safer experimentation with new scheduling policies
- Reduces blast radius of configuration errors through better isolation

## Slide 5: Pods: Scheduling Units in Kubernetes

- Pod: group of containers always scheduled together on same machine
- Containers in pod share network namespace and can share volumes
- Enables sidecar patterns like log collectors, proxies, monitoring agents
- Simplifies application deployment compared to managing individual containers
- Reflects real-world patterns of tightly coupled container groups

## Slide 6: Standard Networking Model

- Every pod gets its own IP address visible across the cluster
- Containers within pod communicate via localhost
- Eliminates need for complex port mapping schemes from Borg
- Standard DNS-based service discovery across the cluster
- Simplifies migration from VM-based architectures

## Slide 7: Label Selectors for Loose Coupling

- Labels: arbitrary key-value pairs attached to any object
- Selectors query objects by label criteria instead of rigid hierarchies
- Decouples service definition from pod implementation details
- Enables flexible grouping and dynamic service membership
- Services automatically discover and route to matching pods

## Slide 8: Decoupling Services from Pods

- Service definition separated from pod lifecycle management
- Pods can be created, destroyed, or scaled independently
- Service maintains stable endpoint regardless of pod changes
- Load balancing across all pods matching the selector
- Enables zero-downtime deployments and rolling updates

## Slide 9: Privileged Operations and Security

- Borg allowed privileged operations tied to specific machine identities
- Kubernetes initially also permitted privileged containers for flexibility
- Trade-off between operational flexibility and security boundaries
- Required careful isolation and admission control policies
- Ongoing evolution toward stricter security models

## Slide 10: Implementation Philosophy

- Core system provides minimal primitives and extension points
- Advanced features implemented as normal controllers using public API
- Controllers watch for changes and reconcile desired vs actual state
- Encourages ecosystem development without core system bloat
- Examples: ReplicaSets, Deployments, StatefulSets all implemented as controllers

## Slide 11: Question for You

How do you balance operational flexibility with security constraints when designing systems that need to support such high levels of automation?
