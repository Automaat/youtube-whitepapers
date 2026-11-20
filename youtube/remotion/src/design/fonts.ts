import { loadFont as loadFraunces } from "@remotion/google-fonts/Fraunces";
import { loadFont as loadMono } from "@remotion/google-fonts/JetBrainsMono";
import { loadFont as loadSans } from "@remotion/google-fonts/PlusJakartaSans";

const subsets = ["latin", "latin-ext"] as const;

export const SERIF = loadFraunces("normal", { weights: ["500", "600", "700"], subsets: [...subsets] }).fontFamily;
export const SANS = loadSans("normal", { weights: ["400", "500", "600", "700", "800"], subsets: [...subsets] }).fontFamily;
export const MONO = loadMono("normal", { weights: ["400", "500", "700"], subsets: [...subsets] }).fontFamily;
