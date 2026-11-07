# Which menu item lost the most weekly contribution after a supplier price rise?

**Free Excel-first field guide · Shenmei Studio · 7 November 2026**

For independent restaurants managing roughly 10–60 menu items with a manual cost sheet. This guide compares **the change in ingredient cost per serving × portions actually sold**. It does not require POS integration, uploading invoices, a subscription, or a purchase.

**What it measures:** the modeled weekly reduction in *contribution before fixed costs*, if selling prices, portion sizes, other variable costs, and sales quantities do not change. This is **not net profit, cash-flow loss, or proof of actual customer demand**. All numbers below are synthetic teaching examples, not restaurant accounts.

## A reproducible two-supplier example

Assume two supplier changes:

| Supplier input | Old | New | Purchase pack | Assumption |
|---|---:|---:|---|---|
| Chicken | $44 | $50 | 10 lb = 160 oz bought | 75% usable weight after trim/cook, same yield both periods |
| Cooking oil | $18 | $24 | 128 US fl oz | Each dish's stated oil usage is actually consumed; do not treat all fryer oil poured into a vat as consumed per serving |

The chicken pack delivers **160 × 75% = 120 usable oz**. Old chicken cost is **$44 / 120 = $0.366666… per usable oz**, new cost is **$50 / 120 = $0.416666…**. The cost increase is **$0.05 per usable oz**. Oil's increase is **($24 − $18) / 128 = $0.046875 per fl oz**. Fluid ounces and weight ounces are *different units*; never combine their quantities.

Assume three dishes use the two affected ingredients in these serving quantities. Other ingredients and costs are unchanged in this comparison:

| Menu item | Chicken usable oz/serving | Oil fl oz/serving | Portions sold/week | Chicken cost increase/portion | Oil cost increase/portion | Total increase/portion | Weekly contribution reduction |
|---|---:|---:|---:|---:|---:|---:|---:|
| Grilled chicken bowl | 6 | 0.25 | 120 | $0.30 | $0.01171875 | $0.31171875 | **$37.41** |
| Chicken wrap | 4 | 1.00 | 180 | $0.20 | $0.046875 | $0.246875 | **$44.44** |
| Chicken salad | 2 | 0.50 | 90 | $0.10 | $0.02343750 | $0.12343750 | **$11.11** |

**Decision:** the *wrap* has the biggest modeled weekly contribution decline ($44.44), although the *bowl* has the larger increase per serving. This is why ranking dishes only by food-cost percentage or dollar change per plate can misallocate attention.

Rounded displayed rows sum to **$92.96** of weekly affected-ingredient contribution reduction. Using unrounded calculations, the total is **$92.953125 ≈ $92.95**. The one-cent difference is display rounding, not a missing cost. Keep unrounded formulas and round only the display; use unrounded values for totals.

## Build this yourself in Excel (no macros)

Put these numeric inputs in the indicated cells, with currency format for prices and percentage format for the yield:

| Cell | Value | Definition |
|---|---:|---|
| B2 | 44 | Old chicken case price ($) |
| B3 | 50 | New chicken case price ($) |
| B4 | 10 | Chicken case weight (lb) |
| B5 | 75% | Chicken usable yield, as Excel 0.75 |
| B6 | 18 | Old oil pack price ($) |
| B7 | 24 | New oil pack price ($) |
| B8 | 128 | Oil pack size (US fl oz) |

Use row 11 for headers and start your menu entries at **row 12**. Copy formulas down to your final menu row (whether 10, 20, or 60). Columns A–D are manual entry; E–L are formulas:

| Column | Content | Excel formula for row 12 |
|---|---|---|
| A | Dish name | Type name |
| B | Chicken usable weight (oz/serving) | Type numeric oz |
| C | Oil actually used (fl oz/serving) | Type numeric fl oz |
| D | Portions sold in the week | Type numeric units |
| E | Old chicken cost/portion | `=IFERROR($B$2/($B$4*16*$B$5)*B12,"")` |
| F | New chicken cost/portion | `=IFERROR($B$3/($B$4*16*$B$5)*B12,"")` |
| G | Old oil cost/portion | `=IFERROR($B$6/$B$8*C12,"")` |
| H | New oil cost/portion | `=IFERROR($B$7/$B$8*C12,"")` |
| I | Old cost of affected ingredients | `=E12+G12` |
| J | New cost of affected ingredients | `=F12+H12` |
| K | Increase per serving | `=J12-I12` |
| L | **Weekly modeled contribution reduction** | `=K12*D12` |

Enter the three example dishes above in rows 12–14. Expected unrounded L12:L14: **37.40625, 44.4375, 11.109375**. Sum with `=SUM(L12:L14)` = **92.953125**. Filter/sort **the entire A:L table** by L descending so that dish names and inputs stay together.

To handle more suppliers, add separate old/new per-serving ingredient-cost columns for each affected ingredient, normalized to **usable units**. Sum the old and new affected costs; calculate their difference once; multiply by actual weekly portions. If supplier prices **fall**, negative weekly reductions are valid (a modeled contribution improvement).

## Validate before making a menu decision

1. **Match units**: compare the supplier's actual invoiced case size and unit (lb, kg, count, liters), not just the headline case price. One US lb = 16 weight oz. Do not confuse weight oz with fluid oz.
2. **Measure usable yield**: where trim, bones, cooking shrinkage, or waste matter, measure actual usable weight. A change in yield may matter more than a price increase; this example holds yield constant.
3. **Verify what was really consumed**: purchased frying oil, sauce, and batch ingredients require credible per-serving allocation, not a guessed spoonful. Include batch yields and leftovers when relevant.
4. **Use sales, not production estimates**: use a consistent completed-week period; exclude comps, voids, and refunds appropriately. Track changes in mix and unit sales separately.
5. **Do not overclaim the result**: a $44.44 modeled reduction is **not** a $44.44 fall in net profit if price, volumes, labor, packaging, fees, discounts, waste, or taxes also change. For pricing decisions, estimate these changes and local demand.

**What to do next:** check the two highest weekly-impact dishes against recent invoices and measured portions, then decide whether a supplier change, recipe adjustment, or a carefully tested price change is justified. Do not change the whole menu based on a theoretical cost model.

## Optional, clearly disclosed tools

Shenmei Studio publishes this guide and operates the tools below. The educational calculation above stands alone; neither tool is required to use it.

- [Free, no-signup supplier-price-change calculator](https://sites.google.com/view/shenmei-food-cost-calculator) — for checking a single ingredient/portion scenario.
- [Optional free Excel + PDF download](https://payhip.com/b/DqxHS) — Payhip requires an email to complete the free checkout.
- [Optional $19 Menu Margin Lab workbook](https://payhip.com/b/TGKW7) — a paid spreadsheet product; review the current product listing and its actual capacity/limitations before buying. **No automatic invoice import or POS connection is claimed.**

This guide is an educational **DIAGNOSIS_ONLY** resource based on hypothetical numbers; no customer trial, verified savings, ROI, or sales result is implied.
