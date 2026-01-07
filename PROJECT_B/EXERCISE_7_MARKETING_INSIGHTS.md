# EXERCISE 7 - ASSOCIATION RULES: MARKETING INSIGHTS SUMMARY

## We-Commerce Market-Basket Analysis Results

**Analysis Date:** January 4, 2026  
**Dataset:** January 2012 e-commerce events (filtered: 5-30 sessions)  
**Total Transactions Analyzed:** 4,945  
**Unique Products:** 1,750

---

## 1. OPTIMAL CONFIGURATION FOUND

**Target:** At most 30 association rules  
**Best Configuration:**
- **Support:** 0.30% (minimum 14 transactions)
- **Confidence:** 65.00%
- **Rules Found:** 26 (within target!)
- **Frequent Itemsets:** 72

This configuration provides a manageable set of actionable rules while maintaining meaningful statistical confidence.

---

## 2. MARKETING DECISION RECOMMENDATIONS

### 2.1 Homepage & Featured Products (Most Visited)

**Top 10 Products to Feature on Main Page:**

1. **display.category*homepage** - 294 visits (5.95%)
   - *Action:* Keep as primary landing page entry
   
2. **intro*fbpage*link1** - 118 visits (2.39%)
   - *Action:* Promote Facebook integration in homepage

3. **lon_4508** (Leather Boot Castanho Mogno) - 99 visits (2.00%)
   - *Action:* Feature in "Best Sellers" carousel

4. **lon_2125** (Luis Onofre Boots Taupe) - 81 visits (1.64%)
5. **lon_4504** (Green Suede Boots with Lateral Elastic) - 78 visits (1.58%)
6. **lon_4004** (Brown Croco Leather Pumps) - 75 visits (1.52%)
7. **lon_4108** (Bordeaux Croco Leather Boot) - 67 visits (1.35%)
8. **lon_4013** (Beige Stiletto Pumps) - 64 visits (1.29%)
9. **lon_2119** (Boots with Swarovski Crystals) - 61 visits (1.23%)
10. **ipodtouch** - 52 visits (1.05%)

**Key Insight:** Luis Onofre footwear dominates traffic. Consider dedicated landing page for this brand.

---

### 2.2 Cross-Selling Rules (Products to Keep Together)

**STRONGEST ASSOCIATIONS (100% Confidence):**

#### Rule #1: iPad/iPod Touch Bundle (Gaming/Tech Category)
- **IF customer views:** ipad1/2
- **THEN also show:** ipodtouch
- **Confidence:** 100.00% (everyone who views iPad views iPod!)
- **Support:** 51 transactions (1.03%)
- **Action:** Create "Apple Ecosystem" product page with both items together

#### Rule #2: Remote-Controlled Helicopter Package
- **IF customer views:** display.product*ljv_0459*helicopterotelecomandadoatravesiphone3/4/4s
- **THEN also show:** ipad1/2 AND ipodtouch
- **Confidence:** 100.00%
- **Support:** 32 transactions (0.65%)
- **Action:** Bundle these tech products for "iPhone Gaming" category

#### Rule #3: Android Title Link Pattern
- **IF customer views:** eandroid pddtitle*ljv_0459*link2
- **THEN also show:** ipad1/2 AND ipodtouch
- **Confidence:** 100.00%
- **Support:** 17 transactions (0.34%)
- **Action:** Cross-promote iOS products to Android browsers

**HIGH CONFIDENCE ASSOCIATIONS (98%+):**

- **ipodtouch → ipad1/2** (98.08% confidence)
  - *Action:* Add "Customers also viewed iPad" banner on iPod Touch pages

---

### 2.3 Rarely Visited but Often Co-Visited Products

**Key Pattern Discovered:**
- Products with low individual support (<1%) but high co-occurrence (>94% confidence)
- Example: Helicopter toy + iPad/iPod Touch combination
- **Strategy:** These products don't drive traffic alone but create strong upsell opportunities

**Recommendations:**
1. Don't feature rarely visited products on homepage
2. DO show them as recommendations when customer views related high-traffic products
3. Create "Frequently bought together" sections leveraging 94%+ confidence rules

---

### 2.4 Product Placement Strategy by Category

#### A. Tech/Gaming Products (High Association)
**Products to Group:**
- iPad 1/2
- iPod Touch
- iPhone-controlled helicopter
- Android gaming accessories

**Placement:** Dedicated "Mobile Gaming" section

#### B. Luis Onofre Footwear (High Individual Traffic)
**Products to Feature:**
- Boots (lon_4508, lon_2125, lon_4504)
- Pumps (lon_4004, lon_4013)
- Items with Swarovski crystals

**Placement:** Premium footwear category page

---

## 3. SPECIFIC MARKETING ACTIONS

### Immediate Actions (Week 1):
1. ✅ **Create Apple Bundle Page:** Group iPad + iPod Touch together
2. ✅ **Add Cross-Selling Widgets:** Show 26 discovered rules as "Customers who viewed X also viewed Y"
3. ✅ **Redesign Homepage:** Feature top 10 products in hero carousel

### Short-Term (Month 1):
4. **Implement A/B Testing:** Test bundle pages vs separate product pages
5. **Email Campaigns:** Send "Complete Your Set" emails for 100% confidence rules
6. **Navigation Restructure:** Create fast-access links for most visited categories

### Long-Term (Quarter 1):
7. **Personalization Engine:** Use association rules for dynamic recommendations
8. **Inventory Optimization:** Ensure stock availability for co-visited products
9. **Marketing Budget:** Allocate ad spend proportional to product visit frequency

---

## 4. BUSINESS QUESTIONS ANSWERED

### Q1: "Which few products should be kept together on a Web page?"

**Answer:** Products with 100% confidence associations:
- iPad + iPod Touch (MUST be on same page)
- Helicopter toy + Apple devices (gaming bundle)
- Android link entries + iOS products (cross-platform appeal)

**Total: 26 product pair combinations found** (see full list in exercise7_results_maxR30.txt)

---

### Q2: "Which products are rarely visited but often visited together?"

**Answer:** Specialized tech accessories:
- Remote helicopter (32 visits, 0.65% support) BUT 100% co-visited with iPad/iPod
- Android product detail links (17 visits) BUT 94-100% co-visited with iOS products

**Strategy:** Don't waste homepage real estate on these, but ALWAYS show as recommendations

---

### Q3: "Which products are the most visited?"

**Answer:** Homepage category & Luis Onofre footwear dominate:

**Category Leaders:**
- Homepage category: 294 visits (6%)
- Facebook integration: 118 visits (2.4%)

**Product Leaders:**
- lon_4508 (Leather Boot): 99 visits (2%)
- lon_2125 (Taupe Boots): 81 visits (1.6%)
- lon_4504 (Green Boots): 78 visits (1.6%)

**Insight:** Luis Onofre brand drives 40%+ of top product traffic

---

## 5. SUPPORT/CONFIDENCE SPACE EXPLORATION

**Tested Configurations:** 210 combinations
**Support Range:** 0.1% - 10%
**Confidence Range:** 50% - 95%

**Key Finding:** 
- At 0.30% support + 65% confidence → 26 rules (closest to maxR=30)
- Higher support (>2%) yields 0 rules (data too sparse after filtering)
- Lower confidence (<65%) adds noise without business value

**Recommendation:** Use discovered configuration (0.30% support, 65% confidence) for future analyses

---

## 6. TECHNICAL NOTES

### Data Characteristics:
- Original dataset: 415,863 events
- After filtering (5-30 sessions): 19,364 events (95% reduction)
- After basket transformation: 4,945 unique visitor sessions
- This filtering created sparse data → fewer rules

### Algorithm Used:
- FP-Growth (via Orange)
- OneHot encoding for basket analysis
- Apriori principle for itemset mining

### Files Generated:
- `exercise7_results_maxR30.txt` - Complete analysis (359 lines)
- `exercise7_association_rules.py` - Reproducible script
- `transactions_basket.basket` - Input data (Orange format)

---

## 7. NEXT STEPS (Exercise 8)

Create graphical Orange workflow report including:
- Association rules visualization
- Interactive rule explorer
- Confidence vs support scatter plots
- Product network graphs

**Tool:** Orange Data Mining GUI with Association Rules widget

---

## SUMMARY

**Exercise 7 successfully explored the support/confidence parameter space to identify 26 high-quality association rules for We-Commerce.**

**Key Outcomes:**
1. ✅ Identified optimal configuration (0.30% support, 65% confidence)
2. ✅ Found 26 actionable marketing rules (target: ≤30)
3. ✅ Answered all 3 business questions
4. ✅ Provided specific product placement recommendations
5. ✅ Discovered strong Apple product bundle opportunity (100% confidence)

**Expected Business Impact:**
- Increased average order value through cross-selling
- Improved user experience with relevant recommendations
- Optimized homepage real estate allocation
- Data-driven inventory and marketing decisions

---

**Generated:** 2026-01-04  
**Script:** exercise7_association_rules.py  
**Full Results:** exercise7_results_maxR30.txt
