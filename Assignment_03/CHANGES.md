# Assignment 03 — CHANGES

**Name:** 67005140040 **Student ID:** Aung Myo Hlaing

This is the written part of your submission. Explain **what you changed and why**, then record your **prompt log**. Keep before/after snippets to a line or two.

---

## 1 · What I changed

One row per change. Name the OOP concept and say how you checked the behaviour was unchanged.

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products were stored as tuples.| Created a Product class. | Classes | Checked the product information and code. |
| 2 | Order items used simple data. |Created an OrderItem class. |Composition | Checked the order calculations. |
| 3 | Customer tiers used many if/elif conditions. | Created Silver, Gold, and Platinum classes. | Inheritance / Polymorphism | Checked the discount and points |
| 4 | Calculations and printing were together. | Separated calculations into different methods. | Encapsulation | Checked the receipt calculations. |
| 5 | The code had magic numbers. | Used named constants. | Clean code | Checked the calculations. |

## 2 · Short reflection (4–6 sentences)

Which change improved the code the most, and why? Where did keeping the behaviour identical force you to be careful?

The biggest change was using classes for the different parts of the store system. The customer classes made the discount and points easier to manage. I also separated the calculations from the receipt printing. I had to be careful not to change the original behaviour. This assignment helped me understand OOP better.
---

## 3 · Prompt log (Level 2 — required)

Record **every** prompt where AI helped. If you wrote a part yourself, say so in one row. AI-shaped code with an empty log does **not** meet the Level-2 policy.

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | "check my code for errors"| Found errors and missing parts. | Edited  | I checked and fixed the errors. |
| 2 |"check if I missed anything"  | Found missing requirements. | Edited — added the missing parts. | I compared it with the assignment. |
| 3 | "check my classes and methods" | Checked the class structure and methods | Edited — changed some methods. | I checked the code and requirements. |

**Ownership statement.** 
I worked on this assignment myself. I used AI mainly to check errors and help me understand some parts. I checked the suggestions and made the final changes myself. I understand my code and can explain what I changed.

---

## 4 · Before-you-submit checklist

- [$ ] `python Assignment_03.py` prints **PASS**.
- [$ ] No tuples / parallel lists left — products, orders, and items are objects.
- [$ ] No `if tier == ...` chains — tiers are a class family.
- [$ ] Calculation methods **return** values and do not `print`; printing is separate.
- [$ ] Constructors validate state; no leftover `global`; magic numbers are named.
- [$ ] The change table and reflection above are filled in.
- [$ ] The prompt log is complete and the ownership statement is signed.
