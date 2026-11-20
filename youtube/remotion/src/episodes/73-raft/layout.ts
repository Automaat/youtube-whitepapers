import { ring } from "../../design";

export const SERVERS = ["S1", "S2", "S3", "S4", "S5"] as const;
export type Server = (typeof SERVERS)[number];

export const RING_CENTER: [number, number] = [900, 590];
export const RING_RADIUS = 270;
export const NODE_R = 54;
export const RING: Record<Server, [number, number]> = Object.fromEntries(
  ring(RING_CENTER[0], RING_CENTER[1], RING_RADIUS, 5).map((p, i) => [SERVERS[i], p]),
) as Record<Server, [number, number]>;

export const LANE_X1 = 200;
export const LANE_X2 = 1780;
export const RIBBON_Y = 230;
export const LANE_Y: Record<Server, number> = { S1: 340, S2: 460, S3: 580, S4: 700, S5: 820 };

export const LOG_LABEL_X = 230;
export const LOG_X0 = 340;
export const LOG_CELL_W = 150;
export const LOG_CELL_H = 92;
export const LOG_CELL_GAP = 16;
export const LOG_RULER_Y = 250;
export const LOG_ROW_Y: Record<Server, number> = { S1: 300, S2: 420, S3: 540, S4: 660, S5: 780 };
export const logCellX = (index: number): number => LOG_X0 + (index - 1) * (LOG_CELL_W + LOG_CELL_GAP);
