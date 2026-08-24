
# Mistral Study Assistant

A simple command-line study assistant powered by Mistral AI.  
Ask questions and get clear, short explanations with a practice question at the end.

## Features

- Interactive chat loop in the terminal
- Friendly study assistant system prompt
- Conversation memory (keeps previous messages)
- Easy exit with `exit`, `quit`, or `q`
- Clean error handling

## Requirements

- Python 3.8+
- Mistral AI API key

## Installation

1. Clone or download this project.

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install mistralai python-dotenv
```

## Setup

1. Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_api_key_here
```

2. Get your API key from [https://console.mistral.ai](https://console.mistral.ai).

## Usage

Run the script:

```bash
python study_buddy.ipynb
```

Example session:

```
Ask a question or type 'exit' to quit: What is photosynthesis?
Photosynthesis is how plants make food. They use sunlight, water, and carbon dioxide. This creates sugar and oxygen.
Practice: What three things do plants need for photosynthesis?
```

Type `exit`, `quit`, or `q` to stop.

## Project Structure

```
.
├── .env                 # Your API key (do not commit this)
├── study_buddy.ipynb              # Main application
└── README.md
```

## Notes

- The model used is `mistral-small-latest`.
- Temperature is set to `0.3` for more consistent answers.
- Maximum response length is limited to 300 tokens.
- Never share or commit your `.env` file.

## License

MIT
