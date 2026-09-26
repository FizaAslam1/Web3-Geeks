# Task 2 — Conversation Flow Design

Each flow below is a state machine. The same structure becomes the LangGraph nodes in Day 5.
Flows 1-7 are the required flows. Flows 8 and 9 are extra flows added so the agent also handles
sellers and the failure cases (unclear, off-topic, silent, angry, injection) tested in Day 6.

Every flow ends in one of two ways: a booked appointment, or a logged lead with a follow-up. Diagram images are in `diagrams/`.

## 1. Buyer Inquiry

Goal: understand the requirement, present 2-3 grounded options, handle objections, book a visit. The first question also routes rent, invest and sell callers to their own flows.

![1. Buyer Inquiry](diagrams/flow1_buyer.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Ask: buy, rent, invest or sell?"]
    B -->|"Rent"| R["Go to Rental flow"]
    B -->|"Invest"| I["Go to Investment flow"]
    B -->|"Sell"| S["Go to Seller flow"]
    B -->|"Unclear or off-topic"| U["Go to Fallback flow"]
    B -->|"Buy"| C["Ask: city, budget, bedrooms, purpose"]
    C --> D["Search: SQL filter + RAG"]
    D --> E{"Match found?"}
    E -->|"Yes"| F["Present 2-3 top options"]
    E -->|"No"| G["Suggest relaxing budget or area"]
    G --> C
    F --> H{"Interested?"}
    H -->|"Yes"| K["Offer property visit"]
    H -->|"Objection"| J["Objection handling"]
    J --> H
    H -->|"Not interested"| N["Offer callback or new options later"]
    N --> Z["Log lead + goodbye"]
    K --> L["Book appointment"]
    L --> M["Confirm + goodbye"]
```

## 2. Rental Inquiry

Goal: match a rental to budget and preferences, explain deposit and tenancy terms from company records, book a viewing.

![2. Rental Inquiry](diagrams/flow2_rental.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Confirm: looking to rent"]
    B --> C["Ask: city, budget, bedrooms, furnished?"]
    C --> D["Search: SQL filter + RAG"]
    D --> E{"Match found?"}
    E -->|"Yes"| F["Present options + monthly rent"]
    E -->|"No"| G["Ask to adjust criteria"]
    G --> C
    F --> H{"Interested?"}
    H -->|"Yes"| I["Explain security deposit + tenancy terms"]
    H -->|"Objection"| O["Objection handling"]
    O --> H
    H -->|"Not interested"| N["Offer callback or new options later"]
    N --> Z["Log lead + goodbye"]
    I --> J["Book viewing"]
    J --> K["Confirm + goodbye"]
```

## 3. Commercial Property Inquiry

Goal: identify purpose (office, shop, warehouse), size and budget, present options and book a site visit.

![3. Commercial Property Inquiry](diagrams/flow3_commercial.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Confirm: commercial property"]
    B --> C["Ask: purpose - office, shop, warehouse; city, budget, size"]
    C --> D["Search: SQL filter + RAG"]
    D --> E{"Match found?"}
    E -->|"Yes"| F["Present options + location advantages"]
    E -->|"No"| G["Ask to broaden search"]
    G --> C
    F --> H{"Interested?"}
    H -->|"Yes"| I["Book site visit"]
    H -->|"Objection: price or location"| J["Objection handling"]
    J --> H
    H -->|"Not interested"| N["Offer callback or new options later"]
    N --> Z["Log lead + goodbye"]
    I --> K["Confirm + goodbye"]
```

## 4. Investment Inquiry

Goal: understand the investment goal, present options using figures that exist in company records only (no invented returns), explain payment plan and developer, book a consultation.

![4. Investment Inquiry](diagrams/flow4_investment.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Confirm: looking to invest"]
    B --> C["Ask: budget, city, goal - rental income or resale profit"]
    C --> D["Search: SQL filter + RAG + rental data from records"]
    D --> E{"Match found?"}
    E -->|"Yes"| F["Present options with figures from records"]
    E -->|"No"| G["Ask to adjust budget or city"]
    G --> C
    F --> H{"Interested?"}
    H -->|"Yes"| I["Explain payment plan + developer details"]
    H -->|"Objection: trust or builder"| J["Objection handling"]
    J --> H
    H -->|"Not interested"| N["Offer callback or new options later"]
    N --> Z["Log lead + goodbye"]
    I --> K["Book consultation or visit"]
    K --> M["Confirm + goodbye"]
```

## 5. Returning Customer

Goal: recognise the caller by phone number, confirm their name before using any stored details (privacy), then continue from their earlier preferences.

![5. Returning Customer](diagrams/flow5_returning.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Look up caller by phone number"]
    B --> C{"Found in CRM?"}
    C -->|"No or hidden number"| D["Treat as new caller - standard flow"]
    C -->|"Yes"| E["Ask caller to confirm their name"]
    E --> F{"Name matches?"}
    F -->|"No"| D
    F -->|"Yes"| G["Greet by name + refer to past preferences"]
    G --> H["Ask: same requirement or something new?"]
    H -->|"Same"| I["Show updated matches since last call"]
    H -->|"New"| J["Standard Buyer, Rental or Investment flow"]
    I --> K["Continue to booking or objection handling"]
```

## 6. Appointment Rescheduling

Goal: find the existing appointment, check the calendar for the new slot, update Calendar and notify the employee by email.

![6. Appointment Rescheduling](diagrams/flow6_reschedule.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Identify appointment via phone + name"]
    B --> C{"Appointment found?"}
    C -->|"No"| D["Ask for details, search again"]
    D -->|"Found"| E
    D -->|"Not found after 2 tries"| X["Offer human callback"]
    C -->|"Yes"| E["Confirm which appointment"]
    E --> F["Ask new preferred date and time"]
    F --> G["Check calendar availability"]
    G --> H{"Slot available?"}
    H -->|"Yes"| I["Update calendar + email employee"]
    H -->|"No"| J["Offer alternate slots"]
    J --> F
    I --> K["Confirm new time + goodbye"]
```

## 7. Appointment Cancellation

Goal: confirm the cancellation, cancel in Calendar, notify the employee, and softly offer a later rebooking.

![7. Appointment Cancellation](diagrams/flow7_cancel.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Identify appointment via phone + name"]
    B --> C{"Appointment found?"}
    C -->|"No"| D["Ask for details, search again"]
    D -->|"Found"| E
    D -->|"Not found after 2 tries"| X["Offer human callback"]
    C -->|"Yes"| E["Confirm cancellation intent"]
    E --> F{"Confirmed?"}
    F -->|"Yes"| G["Cancel in calendar + notify employee"]
    F -->|"Changed mind"| H["Go to Rescheduling flow"]
    G --> I["Ask if they want to rebook later"]
    I --> J["Log + goodbye"]
```

## 8. Seller Inquiry (extra flow)

Not in the Day 1 list, but the Day 6 test suite includes seller conversations. The agent does not value a property on the call; it captures details and hands over to a senior agent.

![8. Seller Inquiry (extra flow)](diagrams/flow8_seller.png)

```mermaid
flowchart TD
    A["Greeting"] --> B["Confirm: wants to sell or list a property"]
    B --> C["Ask: property type, city, area, size"]
    C --> D["Ask: expected price + caller name and phone"]
    D --> E["Explain: agent does not value property on call"]
    E --> F["Create lead in CRM"]
    F --> G["Offer callback or meeting with senior agent"]
    G --> H["Book meeting or set callback"]
    H --> I["Confirm + goodbye"]
```

## 9. Fallback Handling (shared by all flows)

Covers unclear speech, off-topic talk, silence, angry callers, prompt-injection attempts and the question 'are you an AI?'. Every flow routes here when the caller goes off the expected path.

![9. Fallback Handling (shared by all flows)](diagrams/flow9_fallback.png)

```mermaid
flowchart TD
    A["Caller says something"] --> B{"What happened?"}
    B -->|"Not understood"| C["Ask politely to repeat - max 2 times"]
    C -->|"Still unclear"| H["Offer human callback"]
    B -->|"Off-topic"| D["Politely redirect to real estate"]
    D -->|"Keeps going off-topic"| H
    B -->|"Silence"| E["Gentle prompt: Ji sir, aap line par hain?"]
    E -->|"Silent again"| F["Polite closing line, end call"]
    B -->|"Angry or upset"| G["Acknowledge calmly, do not argue"]
    G --> H
    B -->|"Prompt injection or asks for internal data"| P["Decline politely, continue normally"]
    P -->|"Keeps trying"| Q["End call politely + flag in log"]
    B -->|"Asks: are you an AI?"| AI["Answer honestly, offer to continue or human callback"]
    H --> Z["Log reason + create callback task"]
    Q --> Z
    F --> Z2["Log call as no-response"]
```
