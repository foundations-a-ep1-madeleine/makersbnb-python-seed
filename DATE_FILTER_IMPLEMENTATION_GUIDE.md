# Date Filter Implementation Guide

## Overview

This guide explains how the date range filter feature works on the main spaces listing page. Users can enter check-in and check-out dates to see only spaces that are available for their entire requested date range.

---

## Feature Components

### 1. User Interface (templates/spaces.html)

The filter form sits at the top of the spaces listing page:

```html
<form method="get" action="/spaces" class="date-filter-form">
  <div class="filter-inputs">
    <div class="filter-field">
      <label for="start_date">Check-in</label>
      <input type="date" id="start_date" name="start_date" value="{{ start_date or '' }}">
    </div>
    <div class="filter-field">
      <label for="end_date">Check-out</label>
      <input type="date" id="end_date" name="end_date" value="{{ end_date or '' }}">
    </div>
    <button type="submit" class="filter-button">Search</button>
    {% if start_date or end_date %}
    <a href="/spaces" class="clear-filter">Clear</a>
    {% endif %}
  </div>
</form>
```

**Key Features:**
- Two date inputs (start_date and end_date)
- Values are preserved after filtering using `{{ start_date or '' }}`
- "Clear" button appears only when dates are provided
- Form submits via GET to `/spaces?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`

---

### 2. Backend Logic (app.py)

The `/spaces` route handles both unfiltered and filtered requests:

```python
@app.route('/spaces', methods=['GET'])
@token_required
def get_space(user):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    
    # Get date filter parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # If no dates provided, show all spaces
    if not start_date_str or not end_date_str:
        spaces = space_repo.all()
        return render_template('spaces.html', spaces=spaces, logged_in=isinstance(user, User), 
                             start_date=start_date_str, end_date=end_date_str)
```

#### Step-by-Step Flow:

**Step 1: Extract Query Parameters**
```python
start_date_str = request.args.get('start_date')  # e.g., "2025-11-12"
end_date_str = request.args.get('end_date')      # e.g., "2025-11-14"
```

**Step 2: Handle Missing Dates**
```python
if not start_date_str or not end_date_str:
    # Show all spaces if either date is missing
    spaces = space_repo.all()
    return render_template(...)
```

**Step 3: Parse and Validate Dates**
```python
try:
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
except ValueError:
    # Invalid format - show all spaces with error message
    spaces = space_repo.all()
    return render_template(..., error="Invalid date format")

if start_date > end_date:
    # Invalid range - show all spaces with error message
    spaces = space_repo.all()
    return render_template(..., error="Check-out date must be after check-in date")
```

**Step 4: Filter Spaces by Availability**
```python
availability_repo = AvailabilityRepository(connection)
all_spaces = space_repo.all()
filtered_spaces = []

for space in all_spaces:
    availabilities = availability_repo.find_by_space_id(space.id)
    
    # Expand availability ranges to ISO date set
    available_dates = set()
    for avail in availabilities:
        current = avail.start_date
        while current <= avail.end_date:
            available_dates.add(current.isoformat())
            current += timedelta(days=1)
    
    # Check if all requested dates are available
    current = start_date
    all_dates_available = True
    while current <= end_date:
        if current.isoformat() not in available_dates:
            all_dates_available = False
            break
        current += timedelta(days=1)
    
    if all_dates_available:
        filtered_spaces.append(space)
```

**Step 5: Render Filtered Results**
```python
return render_template('spaces.html', spaces=filtered_spaces, logged_in=isinstance(user, User),
                     start_date=start_date_str, end_date=end_date_str)
```

---

## Visual Flow Diagram

### User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Visits /spaces                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────┐
         │ Are date parameters        │
         │ provided in URL?           │
         └────────┬───────────┬───────┘
                  │ NO        │ YES
                  ▼           ▼
         ┌────────────┐  ┌───────────────────┐
         │ Show ALL   │  │ Parse & Validate  │
         │ spaces     │  │ Dates             │
         └────────────┘  └─────────┬─────────┘
                                   │
                         ┌─────────┴──────────┐
                         │ Valid dates &      │
                         │ start < end?       │
                         └─────┬──────┬───────┘
                         NO    │      │ YES
                         ┌─────┘      └─────┐
                         ▼                   ▼
                  ┌──────────────┐    ┌──────────────────┐
                  │ Show all     │    │ Filter spaces by │
                  │ spaces with  │    │ availability     │
                  │ error msg    │    └────────┬─────────┘
                  └──────────────┘             │
                                               ▼
                                    ┌──────────────────────┐
                                    │ Show filtered spaces │
                                    │ (preserve inputs)    │
                                    └──────────────────────┘
```

---

## Availability Checking Logic - Deep Dive

### Example Scenario

**User searches:** Nov 12-14, 2025 (3 nights)

**Space 1 availability in database:**
- Nov 1-15, 2025
- Dec 1-20, 2025

**Space 2 availability in database:**
- Nov 5-8, 2025
- Nov 20-25, 2025

### Step-by-Step Trace for Space 1

**1. Expand availability ranges to individual dates**

```python
availabilities = [
    Availability(id=1, start_date=2025-11-01, end_date=2025-11-15, space_id=1),
    Availability(id=2, start_date=2025-12-01, end_date=2025-12-20, space_id=1)
]

available_dates = set()

# Process first availability: Nov 1-15
current = 2025-11-01
while current <= 2025-11-15:
    available_dates.add(current.isoformat())  # "2025-11-01"
    current += timedelta(days=1)               # Move to next day

# Process second availability: Dec 1-20
current = 2025-12-01
while current <= 2025-12-20:
    available_dates.add(current.isoformat())  # "2025-12-01"
    current += timedelta(days=1)
```

**Result:** `available_dates` now contains:
```
{
    "2025-11-01", "2025-11-02", "2025-11-03", ..., "2025-11-15",
    "2025-12-01", "2025-12-02", "2025-12-03", ..., "2025-12-20"
}
```

**2. Check if ALL requested dates are in the set**

```python
# User wants: Nov 12-14, 2025
start_date = 2025-11-12
end_date = 2025-11-14

current = 2025-11-12
all_dates_available = True

# Check Nov 12
if "2025-11-12" not in available_dates:  # FALSE - it IS in the set
    all_dates_available = False
    break
current = 2025-11-13

# Check Nov 13
if "2025-11-13" not in available_dates:  # FALSE - it IS in the set
    all_dates_available = False
    break
current = 2025-11-14

# Check Nov 14
if "2025-11-14" not in available_dates:  # FALSE - it IS in the set
    all_dates_available = False
    break
current = 2025-11-15  # Loop ends

# Result: all_dates_available = True
```

**Conclusion:** ✅ Space 1 PASSES the filter (Nov 12-14 is fully covered by Nov 1-15 range)

---

### Step-by-Step Trace for Space 2

**1. Expand availability ranges**

```python
availabilities = [
    Availability(id=3, start_date=2025-11-05, end_date=2025-11-08, space_id=2),
    Availability(id=4, start_date=2025-11-20, end_date=2025-11-25, space_id=2)
]

available_dates = set()

# Process first availability: Nov 5-8
available_dates = {
    "2025-11-05", "2025-11-06", "2025-11-07", "2025-11-08"
}

# Process second availability: Nov 20-25
available_dates = {
    "2025-11-05", "2025-11-06", "2025-11-07", "2025-11-08",
    "2025-11-20", "2025-11-21", "2025-11-22", "2025-11-23", "2025-11-24", "2025-11-25"
}
```

**2. Check if ALL requested dates are in the set**

```python
# User wants: Nov 12-14, 2025
start_date = 2025-11-12
end_date = 2025-11-14

current = 2025-11-12
all_dates_available = True

# Check Nov 12
if "2025-11-12" not in available_dates:  # TRUE - it's NOT in the set!
    all_dates_available = False
    break  # Stop checking immediately

# Result: all_dates_available = False
```

**Conclusion:** ❌ Space 2 FAILS the filter (Nov 12 is not available - it falls in the gap between Nov 8 and Nov 20)

---

## Visual Comparison Table

| Date Range Check | Space 1 (Nov 1-15, Dec 1-20) | Space 2 (Nov 5-8, Nov 20-25) |
|------------------|------------------------------|------------------------------|
| User Request     | Nov 12-14, 2025              | Nov 12-14, 2025              |
| Nov 12 available?| ✅ Yes (in Nov 1-15 range)   | ❌ No (in gap)               |
| Nov 13 available?| ✅ Yes (in Nov 1-15 range)   | ❌ No (in gap)               |
| Nov 14 available?| ✅ Yes (in Nov 1-15 range)   | ❌ No (in gap)               |
| **Result**       | **PASS - Show in results**   | **FAIL - Hide from results** |

---

## Gap Handling Example

**Space 3 has two separate availability periods:**
- Nov 1-5, 2025
- Nov 10-15, 2025

**Gap:** Nov 6-9 is NOT available

**User searches Nov 4-11:**

```
Timeline:
Nov 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15
[✓  ✓  ✓  ✓  ✓][✗  ✗  ✗  ✗][✓   ✓   ✓   ✓   ✓   ✓]
              └──────────────────────┘
              User wants Nov 4-11

Checking:
- Nov 4: ✅ Available (in first range)
- Nov 5: ✅ Available (in first range)
- Nov 6: ❌ NOT available (in gap) → STOP, FAIL
```

**Result:** ❌ Space 3 does NOT appear in filtered results because the requested range spans the gap.

---

## Key Design Decisions

### Why Use a Set for Available Dates?

```python
available_dates = set()  # O(1) lookup time
```

**Advantages:**
1. **Fast lookup:** Checking `if date in available_dates` is O(1) constant time
2. **No duplicates:** Overlapping availability ranges are automatically deduplicated
3. **Simple logic:** Easy to understand and test

**Alternative (not used):** Store availability ranges and check overlaps
- More complex logic with edge cases
- Harder to handle gaps between ranges
- Potential for off-by-one errors

### Why Check EVERY Date in the Range?

```python
current = start_date
while current <= end_date:
    if current.isoformat() not in available_dates:
        all_dates_available = False
        break  # Early exit optimization
    current += timedelta(days=1)
```

This ensures **continuous availability** - not just that some dates are available, but that ALL dates from check-in to check-out are available with no gaps.

**Example why this matters:**
- User books Nov 12-14
- If Nov 13 is unavailable, the space is useless (can't skip a day in the middle)
- Must ensure every single night is available

### Why Preserve Input Values?

```html
<input type="date" name="start_date" value="{{ start_date or '' }}">
```

**User Experience:**
- After filtering, users see their original search criteria
- Can easily adjust dates without retyping from scratch
- "Clear" button provides easy way to reset

---

## Testing Strategy

### Test Categories

1. **No Filter Tests**
   - Verify all spaces show when no dates provided
   - Test with only start date (should show all)
   - Test with only end date (should show all)

2. **Valid Filter Tests**
   - Filter with dates that match some spaces
   - Verify correct spaces appear in results
   - Verify input values are preserved

3. **Edge Cases**
   - Invalid date format
   - Check-out before check-in
   - No spaces match criteria (empty results)

4. **Availability Logic Tests**
   - Partial overlap (space available for some but not all dates)
   - Multiple availability ranges with gaps
   - Exact match (requested dates = availability dates)

### Example Test: Partial Availability

```python
def test_spaces_page_handles_partial_availability_correctly(page, test_web_address, db_connection):
    # Space 1 only available Nov 10-12, 2025
    # User searches Nov 11-13
    # Expected: Space 1 should NOT appear (Nov 13 is missing)
    
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    
    page.fill("#start_date", "2025-11-11")
    page.fill("#end_date", "2025-11-13")
    page.click(".filter-button")
    
    # Space 1 should NOT appear because Nov 13 is not available
    space_cards = page.locator(".space-card-link")
    expect(space_cards).to_have_count(0)
```

---

## Styling (static/styles/style.css)

The filter form uses modern, clean styling:

```css
.date-filter-form {
    max-width: 800px;
    margin: 32px auto 40px;
    padding: 24px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.filter-inputs {
    display: flex;
    align-items: flex-end;
    gap: 16px;
    flex-wrap: wrap;  /* Responsive on mobile */
}

.filter-button {
    background: #FF6B35;  /* Matches brand color */
    color: white;
    /* ... hover effects */
}
```

**Key features:**
- Flexbox layout for responsive design
- Consistent spacing with rest of application
- Orange accent color matches brand identity
- Mobile-friendly with flex-wrap

---

## Performance Considerations

### Current Approach (Linear Search)

```python
for space in all_spaces:  # O(n) spaces
    availabilities = availability_repo.find_by_space_id(space.id)
    # Expand and check dates for each space
```

**Time Complexity:** O(n × m × d)
- n = number of spaces
- m = average availability ranges per space
- d = number of days in date range

**For typical usage:**
- 10-100 spaces
- 1-5 availability ranges per space
- 1-14 days in search range
- **Total operations:** < 10,000 (acceptable for web request)

### Potential Optimizations (Not Implemented)

1. **Database-level filtering:**
   ```sql
   SELECT DISTINCT space_id FROM availabilities
   WHERE NOT EXISTS (
       -- Complex query to check date range coverage
   )
   ```
   - More complex SQL
   - Harder to maintain
   - May not be faster for small datasets

2. **Caching expanded dates:**
   - Store pre-expanded date sets in cache
   - Invalidate on availability updates
   - Adds complexity for marginal gain

**Decision:** Keep simple linear search - easy to understand, test, and maintain. Optimize later if performance becomes an issue.

---

## Integration with Calendar Feature

1. **User searches dates on listing page** → Sees only available spaces
2. **Clicks on a space** → Views detailed calendar
3. **Selects specific dates** → Books those dates

**Flow:**
```
/spaces?start_date=2025-11-12&end_date=2025-11-14
         ↓ (filter shows only available spaces)
/spaces/1?year=2025&month=11
         ↓ (view calendar with green/grey dates)
/spaces/1/book (with selected_dates)
         ↓ (create booking)
```

