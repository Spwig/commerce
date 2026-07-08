---
slug: bookable-products
title_i18n_key: Bookable Products
category: products
component: catalog
keywords:
  - bookable
  - booking
  - appointment
  - reservation
  - rental
  - accommodation
  - class
  - event
  - waitlist
  - schedule
  - calendar
  - time slot
  - booking configuration
  - deposit
  - cancellation
url_patterns:
  - /admin/catalog/booking/
  - /admin/catalog/bookingwaitlist/
  - /admin/catalog/bookingconfig/
  - /admin/catalog/product/
related:
  - add-product
  - product-variants
  - managing-customer-accounts
published: true
---

Bookable products let customers reserve a specific date and time when they purchase. This supports appointments, rentals, classes, events, and accommodation bookings — all managed directly from your Spwig admin.

## Booking types

| Type | Best for |
|------|----------|
| **Appointment** | Services: consultations, haircuts, personal training |
| **Rental** | Equipment hire, vehicle rental, room hire |
| **Class / Workshop** | Group sessions with a set capacity |
| **Accommodation** | Multi-night stays with check-in/check-out times |
| **Event** | Ticketed one-time or recurring events |

## Setting up a bookable product

### Step 1: Create the product

1. Navigate to **Products > All Products** and click **+ Add Product**
2. Set **Product Type** to **Booking Product**
3. Complete the standard product fields (name, description, price)
4. Save the product

### Step 2: Configure booking settings

After saving, a **Booking Configuration** section appears on the product edit form. Fill in the booking settings:

#### Booking type and duration

- **Booking Type** — Select the type that best matches your service (Appointment, Rental, Class, etc.)
- **Duration Type** — Choose **Fixed Duration** for set-length sessions, or **Customer Selects Duration** to let customers choose how long they need
- **Duration** and **Duration Unit** — Set the length (e.g., `60` minutes, `1` hour, `2` days)
- **Min/Max Duration** — If customers can select duration, set the allowed range

#### Buffer time

Buffer time is added automatically between bookings to allow for preparation or cleaning:
- **Buffer Before** — Minutes reserved before the booking starts
- **Buffer After** — Minutes reserved after the booking ends

For example, a 60-minute massage appointment with a 15-minute buffer after gives 15 minutes to prepare for the next customer.

#### Advance booking window

- **Minimum Advance Notice** — How far ahead a customer must book (e.g., `24 hours` so same-day bookings are not allowed)
- **Maximum Advance Window** — How far in the future customers can book (e.g., `365 days`)

#### Capacity

- **Max Bookings Per Slot** — For classes and events, set how many customers can book the same time slot. Set to `1` for private appointments.

#### Confirmation

- **Require Manual Confirmation** — When checked, bookings are not automatically confirmed. You must manually approve each booking from the bookings list. Useful when you want to vet customers before confirming.

#### Cancellation policy

- **Cancellation Allowed** — Whether customers can cancel their booking
- **Cancellation Deadline** — How many hours/days before the booking customers can cancel (e.g., `24 hours`)

#### Calendar display

How customers select their date and time on the product page:

| Display Mode | Best for |
|-------------|----------|
| **Calendar View** | General use — full monthly calendar |
| **Date Picker** | Simple single-date selection |
| **Available Dates Dropdown** | Products with limited availability slots |
| **Date Range Picker** | Accommodation and multi-day rentals |

#### Deposits

To require a deposit at checkout instead of full payment:
1. Check **Deposit Enabled**
2. Set **Deposit Type** to **Fixed Amount** or **Percentage of Total**
3. Enter the **Deposit Amount** (e.g., `50` for $50, or `25` for 25%)

#### Accommodation-specific settings

For accommodation bookings, additional fields appear:
- **Check-in Time** and **Check-out Time** — Standard times for the property
- **Standard Occupancy** — Default number of guests included in the base rate

### Step 3: Add booking resources (optional)

Resources are the physical items or staff members that get assigned to a booking — for example, "Room 1", "Court A", or "Instructor Sam".

1. On the product edit form, go to the **Booking Resources** section
2. Click **Add Resource**
3. Give the resource a **Name** and set its **Capacity** (how many bookings it can handle simultaneously)
4. Optionally add resource images

Resources let you track availability per individual asset or staff member, not just per time slot.

### Step 4: Set availability rules

Availability rules define when bookings can be made:

1. Under the product's **Availability** section, click **Add Availability Rule**
2. Select the **Resource** this rule applies to
3. Set the **Days of Week** when bookings are available
4. Set **Start Time** and **End Time** for the available window
5. Optionally set a date range (**Valid From** / **Valid Until**) for seasonal availability
6. Save

## Viewing and managing bookings

### Bookings list

Navigate to **Catalog > Bookings** to see all bookings. You can filter by:
- Status (Pending Confirmation, Confirmed, Cancelled, Completed, No Show)
- Product
- Date range

### Booking statuses

| Status | Meaning |
|--------|---------|
| **Pending Confirmation** | Awaiting manual approval (if confirmation required) |
| **Confirmed** | Booking is confirmed and active |
| **Cancelled** | Booking was cancelled by customer or you |
| **Completed** | The booking date has passed and it was fulfilled |
| **No Show** | Customer did not attend |

### Confirming a pending booking

1. Open the booking from **Catalog > Bookings**
2. Change **Status** to **Confirmed**
3. Save — the customer receives a confirmation email automatically

### Cancelling a booking

1. Open the booking
2. Change **Status** to **Cancelled**
3. Enter a **Cancellation Reason** (shown in the customer's email)
4. Save

## Managing the waitlist

When a time slot is fully booked, customers can add themselves to the waitlist. Spwig notifies waitlisted customers automatically when a cancellation creates an opening.

### Viewing the waitlist

Navigate to **Catalog > Booking Waitlist** to see all waitlist entries. Each entry shows:
- Customer name and email
- The product and desired date
- Status: **Waiting**, **Notified**, **Converted to Booking**, or **Expired**

### Waitlist statuses

| Status | Meaning |
|--------|---------|
| **Waiting** | Customer is queued, slot not yet available |
| **Notified** | Customer has been emailed about an available slot |
| **Converted to Booking** | Customer took the slot and completed a booking |
| **Expired** | The desired date passed without a slot becoming available |

### Manually notifying a waitlisted customer

If you want to contact a specific waitlisted customer before the automatic notification:
1. Open the waitlist entry
2. Copy their email address and contact them directly
3. Once they complete a booking, their waitlist entry status updates to **Converted to Booking**

## Tips

- Enable manual confirmation for high-value bookings (e.g., photography sessions, private events) so you can check availability and match requirements before committing.
- Set buffer time generously to start — you can always reduce it once you understand real-world turnaround needs.
- For group classes, set **Max Bookings Per Slot** to the class capacity and enable the waitlist so popular sessions automatically build a queue.
- Use the date range picker display mode for accommodation products — customers expect to select arrival and departure dates together.
- Set a minimum advance notice to prevent last-minute bookings if you need preparation time (e.g., 48-hour minimum for custom catering orders).
- Review your waitlist regularly during busy seasons — manual outreach to waitlisted customers can fill cancellations faster than the automatic notification.
