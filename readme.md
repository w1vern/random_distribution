
# Student Presentation Order Generator

This script assigns an optimal presentation order based on student preferences and unavailable slots.

## Usage

1. Create input file:
   ```bash
   .exe create N
   ```
   Creates `input.json` for `N` students.

2. Fill `input.json` with:
   - `name`: student name or number
   - `choice`: preferred position (1-based)
   - `unavailable_places`: e.g., `"1,2,5-7"`

3. Generate result:
   ```
   .exe calc
   ```
   Outputs result to `output.txt`.

## Output Format

In `output.txt`:
- **1st column**: presentation order
- **2nd column**: student number from input list

Example:  
`2. 11` → 11th student will present 2nd.

---
