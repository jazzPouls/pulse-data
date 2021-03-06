// Recidiviz - a data platform for criminal justice reform
// Copyright (C) 2021 Recidiviz, Inc.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
// =============================================================================

export const titleCase = (str: string): string => {
  // Step 1. Lowercase the string
  // Step 2. Split the string into an array of strings
  const split: string[] = str.toLowerCase().replace(/_/g, " ").split(" ");
  // str = "i'm a little tea pot".split(' ');

  // Step 3. Create the FOR loop
  for (let i = 0; i < split.length; i += 1) {
    split[i] = split[i].charAt(0).toUpperCase() + split[i].slice(1);
  }
  // Step 4. Return the output
  return split.join(" "); // ["I'm", "A", "Little", "Tea", "Pot"].join(' ') => "I'm A Little Tea Pot"
};

// Returns a base64-encoded SHA-256 hash of the input string. Adapted from:
// https://stackoverflow.com/questions/18338890/are-there-any-sha-256-javascript-implementations-that-are-generally-considered-t
export const sha256 = async (message: string): Promise<string> => {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  return btoa(String.fromCharCode(...new Uint8Array(hashBuffer)));
};
