import { createContext, useContext } from "react";
import { THEMES, type Theme } from "./tokens";

export const ThemeContext = createContext<Theme>(THEMES.dark);

export const useTheme = (): Theme => useContext(ThemeContext);
