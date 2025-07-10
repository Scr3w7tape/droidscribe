Agent Blueprint: Simple Dice Roller
Project: Simple Dice Roller
Version: 1.0
Author: Droidscribe

1. Overview
This document specifies the requirements for a single-screen Android application built with Jetpack Compose. The application will allow a user to simulate rolling a standard six-sided die and see the result on the screen.

2. Core Functionality
The application consists of a single screen with the following components and logic:

State Management:

The UI must hold one piece of state: the current value of the die.

This state should be managed by a mutableStateOf<Int> variable, initialized to 1.

UI Components:

Result Display: A Text composable that displays the current die value.

The text should be large for visibility (e.g., fontSize = 60.sp).

Roll Button: A Button composable with the label "Roll".

Interaction Logic:

When the "Roll" button is clicked, a new random integer between 1 and 6 (inclusive) must be generated.

The diceValue state must be updated with this new random number, causing the Text composable to recompose and display the new result.

3. UI Layout and Structure
The UI should be implemented within a single @Composable function, DiceRollerApp.

The root composable should be a Column.

The Column must fill the entire screen (modifier = Modifier.fillMaxSize()).

The contents of the Column must be centered both vertically and horizontally (verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally).

A Spacer with a height of 16.dp should be placed between the result Text and the "Roll" Button for visual separation.

4. Code Generation Requirements
Target File: The AI must generate the complete code for the app/src/main/java/com/example/generatedapp/MainActivity.kt file.

Package: The package name must be com.example.generatedapp.

Imports: All necessary Jetpack Compose imports (Column, Button, Text, mutableStateOf, remember, etc.) MUST be included.

Theme: The root composable should be wrapped in the GeneratedAppTheme provided by the template.
