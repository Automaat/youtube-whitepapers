Generate 11 presentation slides based on the podcast about Apache Kafka.

## Visual Style

- Minimal, clean design with dark blue headers
- White/light gray background
- Sans-serif typography throughout
- Simple outline icons only (no stock photos, no AI-generated images)
- Consistent layout: title at top, bullets left-aligned
- Same spacing and margins across all slides
- Use diagrams/flowcharts for technical concepts where appropriate

---

## Slide 1: Kafka Origins at LinkedIn

- Developed at LinkedIn to handle massive data streams
- Traditional message brokers (ActiveMQ, RabbitMQ) couldn't scale
- Needed system for log aggregation and real-time data pipelines
- Design focused on high throughput over low latency
- Open-sourced to become industry standard messaging platform

## Slide 2: Core Architecture Principles

- Topic-based publish-subscribe model
- Messages organized into topics (logical channels)
- Topics divided into partitions for parallelism
- Each partition is ordered, immutable sequence of messages
- Producers write to topics, consumers read from topics

## Slide 3: Append-Only Log Structure

- Partitions implemented as append-only logs
- Sequential disk writes for maximum throughput
- Messages never modified after written
- Simple offset-based addressing within partition
- Efficient for both producers and consumers

## Slide 4: Consumer Pull Model

- Consumers pull messages at their own pace
- Inverted from traditional message broker push model
- Consumers maintain their own offset position
- Can replay messages by resetting offset
- Enables independent consumer scaling and recovery

## Slide 5: Zero-Copy Transfer Optimization

- Uses operating system page cache aggressively
- Zero-copy transfer from disk to network socket
- Avoids multiple data copies through application layer
- Dramatically reduces CPU overhead
- Key to achieving high throughput performance

## Slide 6: Partition Replication

- Each partition replicated across multiple brokers
- Leader replica handles reads and writes
- Follower replicas sync data from leader
- Automatic failover when leader fails
- Configurable replication factor for durability

## Slide 7: Consumer Groups

- Multiple consumers organized into groups
- Each partition assigned to single consumer in group
- Enables parallel processing of topic data
- Automatic rebalancing when consumers join/leave
- Combines queuing and pub-sub patterns

## Slide 8: Message Retention Policy

- Messages retained for configurable time period
- Default 7 days, can be extended indefinitely
- Retention independent of consumption
- Enables multiple consumer applications on same data
- Can replay historical data within retention window

## Slide 9: Performance Characteristics

- Throughput: 4x faster than RabbitMQ and ActiveMQ
- Handles millions of messages per second
- Linear scalability by adding brokers and partitions
- Low overhead per message
- Optimized for batch processing of data streams

## Slide 10: Use Cases and Impact

- Log aggregation across distributed systems
- Real-time analytics and monitoring pipelines
- Event sourcing architectures
- Stream processing with Kafka Streams
- Foundation for modern data infrastructure at scale

## Slide 11: Question for You

Have you encountered situations where traditional message brokers couldn't handle your data volume, and how did Kafka's architecture solve those challenges?
