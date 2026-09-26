# Day 3 — Barge-in Design

## Requirement
Agent must stop speaking immediately when the caller interrupts.

## Status
- **Design:** complete (documented in notebook + this file)
- **Simulation:** state machine tested (3 scenarios)
- **Live implementation:** scheduled for Day 7 (needs real audio I/O)

## Components for Day 7
- `sounddevice` for real-time mic capture
- `webrtcvad` (or Silero VAD) for voice activity detection
- ElevenLabs **streaming** endpoint for interruptible TTS
- Shared flag between TTS thread and VAD thread

## Scenarios tested in simulation
1. No interruption: agent speaks fully, then resumes listening
2. Interruption: agent stops mid-sentence, hands back to STT
3. False positive: caller speaks while agent is silent — no action
