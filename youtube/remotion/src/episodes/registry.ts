import type { FC } from "react";
import { scenes as raft } from "./73-raft/scenes";

/** Episode slug → scene id → scene component. */
export const EPISODES: Record<string, Record<string, FC>> = {
  "73-raft": raft,
};
