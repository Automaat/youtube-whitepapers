Generate 11 presentation slides based on the podcast about "Programming Semantics for Multiprogrammed Computations" by Dennis and Van Horn (1966).

## Visual Style
- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Multiprogramming in 1966
- Room-sized computers costing a fortune, processor time as the most precious resource
- Revolutionary idea: one powerful machine running multiple programs simultaneously
- Published in Communications of the ACM, March 1966 by Jack B. Dennis and Earl C. Van Horn (MIT)
- Foundation for modern operating systems and digital world architecture
- Challenge: sharing expensive hardware while maintaining safety and isolation

## Slide 2: Supervisor Calls - The OS Interface Layer
- Supervisor calls act as bridge between assembly language and high-level languages
- Interface for programmers to communicate with OS about fundamental operations
- Creating new tasks, protecting memory, and sharing resources
- Operating between low-level assembler and high-level programming languages
- Protection as the central theme throughout the entire paper

## Slide 3: Segments - Named Memory Objects
- Departure from thinking of memory as one long sequence of addresses
- Information organized into logical, named units called segments
- Segment can be procedure, data array, or any logical unit
- Not raw memory chunk but object with its own identity
- Tree-structured organization replacing flat memory model

## Slide 4: Access Control Lists (ACL)
- Each segment has attached ACL defining who can do what
- Three permission types: R (read), W (write), X (execute)
- User attempting to read segment needs R permission in ACL
- Administrative simplicity - permissions stored with resources
- Easy to answer "who has access to this file?" question

## Slide 5: Capabilities - Bearer Tokens for Access
- Unforgeable tokens granting specific rights to specific segments
- Process holding capability with RW to segment 42 can read and write to it
- Like keys that cannot be counterfeited, providing precise access control
- More flexible than ACL for dynamic permission management
- Security through possession rather than identity verification

## Slide 6: Fork - Creating New Processes
- Fork operation creates almost perfect copy of parent process
- Child process inherits parent's memory space and execution context
- Makes multiprogramming nearly transparent to programmers
- Fundamental building block for concurrent program execution
- Enables process hierarchy and resource inheritance

## Slide 7: Atomic Operations and Synchronization
- LOG and UNLOG primitives for synchronization between processes
- Operations must be atomic and uninterruptible
- Ensures consistency when multiple processes access shared resources
- Critical sections protected from concurrent modifications
- Foundation for building higher-level synchronization mechanisms

## Slide 8: Hierarchical Process Management
- Control returns to large supervisor managing all processes
- Processes organized in tree structure with parent-child relationships
- Paths in tree structure represent process hierarchies
- Supervisor maintains process table and scheduling information
- Hierarchical model enables resource quotas and access control

## Slide 9: ACL vs Capabilities - Two Security Models
- ACL model: permissions attached to resources (won historically)
- Capabilities model: permissions held by processes (more precise)
- ACL conceptually simpler to implement and understand for administrators
- Capabilities provide formal security guarantees and principle of least privilege
- Debate continues: which model better fits modern security needs?

## Slide 10: Modern Relevance and Historical Circle
- Identified fundamental properties of secure multiprogramming systems
- ACL model dominates in Unix permissions, file systems, cloud IAM
- Capabilities returning in microservices, containerization, WebAssembly
- Each component receiving only minimal necessary permissions
- Ideas from 1966 remain alive in today's infinitely more complex world

## Slide 11: Question for You
And today? In the era of infinitely more complex and dangerous digital world, are we witnessing the silent return of capability-based thinking?
