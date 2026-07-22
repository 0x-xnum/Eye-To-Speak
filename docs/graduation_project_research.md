# Eye-To-Speak: AAC and Eye-Tracking Research

This document compiles the research, analytics, and architectural decisions made for the "Eye-To-Speak" graduation project. It serves as a foundational reference for the project's design choices regarding user accessibility, cognitive load, and pattern recognition.

---

## 1. The Problem with Morse Code

Initially, eye-tracking assistive technologies relied heavily on spelling out words character by character using Morse code. While functional, clinical research into Augmentative and Alternative Communication (AAC) highlights severe drawbacks:
*   **High Cognitive Load:** The user must memorize 26 distinct patterns (one for each letter).
*   **Physical Exhaustion:** Spelling a simple word like "WATER" requires up to 15 deliberate blinks, leading to rapid eye fatigue.
*   **Speed:** Morse code via blinking typically yields less than 2 Words Per Minute (WPM) for novice users.

---

## 2. Alternatives to Morse Code

To alleviate these issues, modern AAC systems utilize several advanced techniques:

### A. Dwell-Time Typing
Used by commercial systems like Tobii Dynavox. The user looks at an on-screen keyboard and stares (dwells) at a letter for ~800ms to select it.
*   **Pros:** Highly intuitive (5–15 WPM).
*   **Cons:** Causes the "Midas Touch" problem, where the user accidentally clicks items they are merely reading, causing frustration.

### B. Continuous Gaze Navigation (e.g., Dasher)
A predictive interface where letters stream across the screen, and the user "steers" their gaze toward the desired letter.
*   **Pros:** Fast (15–25 WPM) and eliminates the Midas Touch problem.
*   **Cons:** High learning curve; feels like steering a vehicle with the eyes.

### C. Pattern-to-Phrase Mapping (The Selected Approach)
Instead of spelling words, specific blink patterns are mapped directly to essential phrases (Core Vocabulary). This drastically reduces the number of blinks required for immediate needs.

---

## 3. Cognitive Load Theory & Semantic Compaction

When designing a pattern-to-phrase dictionary, we must rely on **Motor Automaticity** (muscle memory). According to AAC principles like Semantic Compaction (used in Minspeak), an effective dictionary follows three rules:

1.  **Semantic Grouping:** Group phrases by category using the *first blink* as the selector. (e.g., all patterns starting with a Short blink are Conversational).
2.  **The 3-Blink Limit:** Patterns must never exceed 3 blinks. Anything longer becomes a conscious math problem rather than muscle memory.
3.  **Mnemonic Associations:** Give the user a logical story for the pattern (e.g., `Long-Short` = "Long craving, short sip of water").

---

## 4. The Final Dictionary Design

Based on clinical research regarding ALS and locked-in syndrome, patients primarily need quick access to **Core Vocabulary** and **Emergency phrases**. We have designed a 9-pattern dictionary and 1 safety rule.

### The Safety Override (Dead-Man's Switch)
*   **[EYES CLOSED FOR 3 SECONDS]:** `MEDICAL EMERGENCY`
    *   *Rationale:* A panicking or choking patient cannot perform a patterned blink. If the system detects a continuous 3-second eye closure, it immediately triggers an alarm.

### Category 1: Social & Conversational (Starts with Short Blink)
1.  **`S` (1 Short Blink):** "Yes"
2.  **`SS` (2 Short Blinks):** "No"
3.  **`SSS` (3 Short Blinks):** "I don't know / Maybe"
4.  **`SL` (Short-Long):** "Thank You"
5.  **`SLS` (Short-Long-Short):** "Please repeat that"

### Category 2: Personal Needs (Starts with Long Blink)
6.  **`L` (1 Long Blink):** "I need help"
7.  **`LS` (Long-Short):** "I am thirsty or hungry"
8.  **`LL` (Long-Long):** "I am uncomfortable, please move me"

### Category 3: System Control
9.  **`LSS` (Long-Short-Short):** "Open Keyboard Mode" (Switches the application to a visual scanning mode for spelling custom words).

---

## 5. Open Source Inspiration

The project draws inspiration from **OptiKey**, a free, open-source AAC application for Windows. Like OptiKey, "Eye-To-Speak" aims to provide a robust, low-cost alternative to expensive proprietary systems by relying on standard webcams and accessible computer vision libraries (OpenCV, MediaPipe) rather than specialized hardware.
