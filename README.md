# GROUP NAME
This is a project based on TikTok TechJam 2024

## Background
TikTok livestreams have recently surged in popularity, providing an accessible platform for creators to share their interests and hobbies with a wide audience.

## Problem Statement (Inspiring Creativity with Generative AI)
High-traffic live streams, which attract hundreds or even thousands of viewers, are challenging to manage. The primary appeal of livestreaming is the live interaction between the creator and the audience. However, due to the sheer volume of messages in the chat or the creator's focus on content creation, viewers may feel neglected or may struggle to have their questions answered.

## Goals and Objectives
- **Enhance creators’ efficiency and the quality of their creation.**
- **Improve the consumption experience for consumers.**

## Current State
Currently, many creators either do nothing to manage the overwhelming chat traffic or hire an additional admin to handle chat interactions.

## Proposed Solution
We propose utilizing Generative AI, specifically Large Language Models (LLM), to manage the chat by employing a chat assistant to monitor and react to messages. This LLM chat agent can replace the admin, providing timely and relevant responses to the chat as defined by the streamer. With the implementation of an LLM chat agent, creators can focus on their content creation and enrich their chat with interactions.

## Features

### 1. Summarization
The LLM can summarize the sentiment, mood, and content of the chat, providing creators with a quick overview of the ongoing conversation. This allows creators to directly interact with viewers based on the summarized information.

### 2. Aspect-Based Sentiment Analysis (ABSA)
ABSA enables the LLM to analyze specific aspects of the chat messages, identifying sentiments related to particular topics or products. This helps creators understand the audience's opinions and feelings towards specific subjects discussed during the livestream.

### 3. Auto Replies
The LLM chat assistant can automatically respond to viewer questions and comments in real-time. This ensures that viewers receive timely and relevant responses, even when the creator is focused on content creation.

#### Example of Interaction
**Viewer Question:** "Is the shirt available in black?"

**LLM Agent Response:** "Yes, there are 3 colors available: black, white, and blue."
