---
name: ghost-auto-trader
description: Architect and deploy the Ghost Auto-Trader framework: a zero-DTE options trading pipeline using TradingView webhooks, AI-gate validation, and broker execution.
---

# Ghost Auto-Trader Architecture

This skill helps you deploy the Ghost Alpha Trading System for 0DTE options.

## Architecture Pipeline
1. **Signal Generation:** TradingView fires a "Ghost Alpha Grade A" alert based on momentum squeeze metrics.
2. **Webhook Receiver:** A Python FastAPI/Flask backend receives the signal payload containing ticker, timeframe, grade, and relative volume.
3. **The AI Gate:** The payload is sent to an LLM (e.g., Gemini Flash) for immediate contextual validation (checking macro alignment and news sentiment).
4. **Execution:** If the AI gate approves, the system automatically buys the ATM/OTM 0DTE option via the broker API (e.g., Tradier).
5. **Position Management:** A rigid 30-second monitor loop enforces +50% Take Profit, -40% Stop Loss, and a hard 3:00 PM ET time-based exit.

## Usage
When the user asks to "set up a trading bot" or "build an auto-trader":
1. Scaffold the `main.py` webhook listener.
2. Scaffold the `auto_trader.py` execution engine with the AI gate.
3. Ensure strict risk management parameters are hardcoded.
