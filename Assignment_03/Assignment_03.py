"""
================================================================================
 Assignment 03 — Refactor the Messy Store System
 192-201 Advanced Computer Programming with Generative AI
 Week 5 — OOP Design & Refactoring   |   Faculty of IT (International), Siam University
 Lecturer: Hrang Kap Lian
================================================================================

 Maps to: CLO1 (object-oriented design) and CLO5 (responsible, verified AI use)
 Weight:  10 Points     AI-use level: Level 2 (AI-assisted + PROMPT LOG required)

--------------------------------------------------------------------------------
 THE TASK
--------------------------------------------------------------------------------
 You are given ONE working program that is badly written. Do NOT add features and
 do NOT change what it does. REFACTOR it: reshape the code into a clean,
 object-oriented design while producing the EXACT SAME output.

   The one rule of refactoring:  same behaviour, cleaner code.
   If the output changes, it is no longer a refactor — it is a bug.

 How to run:
   python Assignment_03.py
 It prints PASS when your refactor reproduces the original output exactly,
 or FAIL with the first line that differs.

--------------------------------------------------------------------------------
 WHAT YOU WILL PRACTISE (use ALL of these)
--------------------------------------------------------------------------------
   Week 2  Model data as CLASSES with attributes and methods (not tuples/lists).
   Week 3  ENCAPSULATION — validate object state in the constructor.
   Week 4  INHERITANCE & POLYMORPHISM — replace the `if tier == ...` chains
           with a family of classes.
   Week 5  COMPOSITION (has-a) — an Order has-a customer and has-many items;
           an item has-a product.
   Week 5  PURE FUNCTIONS vs MODIFIERS — calculation methods RETURN values and
           print nothing; keep them separate from the receipt printing.
   Week 5  INTERFACE vs IMPLEMENTATION — separate WHAT the receipt shows from
           HOW the totals are computed.

--------------------------------------------------------------------------------
 RULES
--------------------------------------------------------------------------------
 1. Behaviour must stay identical — the self-test must print PASS.
 2. Refactor only. No new discounts, no prettier receipts, no extra products.
 3. You choose the class design — there is no single correct answer.
 4. Level-2 AI use: you may use AI to explain/suggest/refactor, but YOU verify
    every change and you keep a PROMPT LOG (in CHANGES.md).
 5. Work in small steps: change one thing -> run -> keep it green.

--------------------------------------------------------------------------------
 THE SCENARIO
--------------------------------------------------------------------------------
 A small online store prints a receipt per order and a grand total. Business rules:
   - Tax: electronics & stationery = 7%; food = tax-free.
   - Membership discount on the subtotal:
         tier      subtotal<=100   subtotal>100
         none        0%              0%
         silver      2%              5%
         gold        5%              10%
         platinum    10%             15%
   - Bulk discount: 10+ items in total -> add another 3% of the subtotal.
   - total = subtotal - discount + tax
   - points = int(total // 10) * tier_multiplier   (none x1, silver x2, gold x3, platinum x5)
 You do not change these rules — you express them cleanly.

--------------------------------------------------------------------------------
 YOUR TASKS  (see the rubric at the bottom)
--------------------------------------------------------------------------------
   A. (required) Model the domain with classes + composition
                 e.g. Product, OrderItem (has-a Product), Customer, Order.
   B. (required) Encapsulate & validate state in constructors (e.g. qty >= 1).
   C. (required) Replace the tier `if/elif` chains (discount AND points) with
                 polymorphism — a class family, no `if tier == ...`.
   D. (required) Separate calculation from printing: pure methods return numbers.
   E. (required) Kill magic numbers (name them) and remove the leftover `global`.
   F. (stretch)  Let each product decide its own tax — no `if category` in totals.
   G. (stretch)  Add a sensible __str__ where it helps.

--------------------------------------------------------------------------------
 SUBMIT
--------------------------------------------------------------------------------
   1) This file, Assignment_03.py, with your refactor (self-test prints PASS).
   2) CHANGES.md — your written explanation of each change + your prompt log.
================================================================================
"""

import io
import contextlib


# ==============================================================================
#  LEGACY STORE SYSTEM  —  messy but working.   DO NOT EDIT THIS SECTION.
#  Read it, understand it, and use its output as the correct behaviour.
# ==============================================================================
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]
TAXRATE = 0.07
foodtax = 0.0
ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]; t = o[1]; items = o[2]
    sub = 0.0; tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]; q = it[1]
        p = PRODUCTS[pi][1]; nm = PRODUCTS[pi][0]; cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100: d = sub * 0.05
        else: d = sub * 0.02
    elif t == "gold":
        if sub > 100: d = sub * 0.10
        else: d = sub * 0.05
    elif t == "platinum":
        if sub > 100: d = sub * 0.15
        else: d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none": pts = int(total // 10)
    elif t == "silver": pts = int(total // 10) * 2
    elif t == "gold": pts = int(total // 10) * 3
    elif t == "platinum": pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in ORDERS:
        grand = grand + calc(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
#  BEHAVIOUR LOCK  —  DO NOT EDIT.
#  Captures the exact output of the legacy program as the target you must match.
# ==============================================================================
def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
#  YOUR REFACTORED SOLUTION  —  WRITE YOUR CODE BELOW.
#  Design your own classes. A suggested skeleton is commented out — change freely.
#  Your program must define refactored_main() which PRINTS the same output.
# ==============================================================================
TAX_RATE = 0.07
FOOD_TAX = 0.0
DISCOUNT_LIMIT = 100.0
BULK_LIMIT = 10
BULK_RATE = 0.03
POINTS_DIVISOR = 10

SILVER_BASE_RATE = 0.02
SILVER_HIGH_RATE = 0.05
GOLD_BASE_RATE = 0.05
GOLD_HIGH_RATE = 0.10
PLATINUM_BASE_RATE = 0.10
PLATINUM_HIGH_RATE = 0.15

SILVER_MULTIPLIER = 2
GOLD_MULTIPLIER = 3
PLATINUM_MULTIPLIER = 5


class Product:
    """Represents a store product with category-based tax rules."""

    def __init__(self, name: str, price: float, category: str):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price
        self.category = category
        self.tax_rate = FOOD_TAX if category == "food" else TAX_RATE

    def get_tax(self, amount: float) -> float:
        return amount * self.tax_rate

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"


class OrderItem:
    """Represents a line item with quantity validation and pricing methods."""

    def __init__(self, product: Product, quantity: int):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self.product = product
        self.quantity = quantity

    def get_price(self) -> float:
        return self.product.price * self.quantity

    def get_tax(self) -> float:
        return self.product.get_tax(self.get_price())

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity} = {self.get_price()}"


class Customer:
    """Base customer class for standard members."""

    def __init__(self, name: str):
        if not name:
            raise ValueError("Customer name cannot be empty")
        self.name = name

    @property
    def tier_name(self) -> str:
        return "none"

    def get_discount(self, subtotal: float) -> float:
        return 0.0

    def get_multiplier(self) -> int:
        return 1


class Silver(Customer):
    @property
    def tier_name(self) -> str:
        return "silver"

    def get_discount(self, subtotal: float) -> float:
        rate = SILVER_HIGH_RATE if subtotal > DISCOUNT_LIMIT else SILVER_BASE_RATE
        return subtotal * rate

    def get_multiplier(self) -> int:
        return SILVER_MULTIPLIER


class Gold(Customer):
    @property
    def tier_name(self) -> str:
        return "gold"

    def get_discount(self, subtotal: float) -> float:
        rate = GOLD_HIGH_RATE if subtotal > DISCOUNT_LIMIT else GOLD_BASE_RATE
        return subtotal * rate

    def get_multiplier(self) -> int:
        return GOLD_MULTIPLIER


class Platinum(Customer):
    @property
    def tier_name(self) -> str:
        return "platinum"

    def get_discount(self, subtotal: float) -> float:
        rate = PLATINUM_HIGH_RATE if subtotal > DISCOUNT_LIMIT else PLATINUM_BASE_RATE
        return subtotal * rate

    def get_multiplier(self) -> int:
        return PLATINUM_MULTIPLIER


TIER_MAP = {
    "silver": Silver,
    "gold": Gold,
    "platinum": Platinum,
}


def create_customer(name: str, tier: str) -> Customer:
    customer_cls = TIER_MAP.get(tier, Customer)
    return customer_cls(name)


class Order:
    """Handles pure calculations and separate I/O receipt rendering."""

    def __init__(self, customer: Customer, items: list[OrderItem]):
        self.customer = customer
        self.items = items

    def subtotal(self) -> float:
        return sum(item.get_price() for item in self.items)

    def discount(self) -> float:
        sub = self.subtotal()
        disc = self.customer.get_discount(sub)
        total_qty = sum(item.quantity for item in self.items)
        if total_qty >= BULK_LIMIT:
            disc += sub * BULK_RATE
        return disc

    def tax(self) -> float:
        return sum(item.get_tax() for item in self.items)

    def total(self) -> float:
        return self.subtotal() - self.discount() + self.tax()

    def points(self) -> int:
        return int(self.total() // POINTS_DIVISOR) * self.customer.get_multiplier()

    def print_receipt(self) -> None:
        print(f"Receipt for {self.customer.name} ({self.customer.tier_name})")
        print("-" * 40)
        for item in self.items:
            print(item)
        print("-" * 40)
        print(f"Subtotal: {round(self.subtotal(), 2)}")
        print(f"Discount: {round(self.discount(), 2)}")
        print(f"Tax: {round(self.tax(), 2)}")
        print(f"Total: {round(self.total(), 2)}")
        print(f"Points earned: {self.points()}")
        print("")


def refactored_main():
    products = [Product(p[0], p[1], p[2]) for p in PRODUCTS]
    grand_total = 0.0

    for o in ORDERS:
        name, tier, order_data = o[0], o[1], o[2]
        customer = create_customer(name, tier)
        items = [OrderItem(products[idx], qty) for idx, qty in order_data]

        order = Order(customer, items)
        order.print_receipt()
        grand_total += order.total()

    print(f"GRAND TOTAL (all orders): {round(grand_total, 2)}")


# ==============================================================================
#  SELF-TEST  —  DO NOT EDIT.   Run:  python Assignment_03.py
# ==============================================================================
def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()


# ==============================================================================
#  RUBRIC (10 pts)
#   Behaviour preserved (self-test PASS) .................. 2
#   Domain modelling & composition ....................... 2
#   Polymorphism (tier discount & points, no if/elif) .... 1.5
#   Pure calculation vs I/O separation ................... 1.5
#   Encapsulation & validation ........................... 1
#   Clean code (names, no magic numbers, DRY, no global).. 1
#   CHANGES.md explanation (per-change, before->after) ...  0.5
#   CHANGES.md prompt log (Level-2) ......................  0.5
#  NOTE: passing the test alone is only 20/100 — most marks are for the DESIGN
#        and for explaining and verifying your changes. 
# ==============================================================================