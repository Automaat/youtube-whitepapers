import type { FC } from "react";
import { scenes as part1 } from "./part1";
import { scenes as part2 } from "./part2";
import { scenes as part3 } from "./part3";
import { scenes as part4 } from "./part4";
import { scenes as part5 } from "./part5";

export const scenes: Record<string, FC> = { ...part1, ...part2, ...part3, ...part4, ...part5 };
