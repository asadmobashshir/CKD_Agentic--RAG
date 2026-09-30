def build_interface() -> gr.Blocks:
    """Construct the Gradio UI."""

    with gr.Blocks(
        title="CKD Agentic RAG Demo",
        theme=gr.themes.Soft()
    ) as demo:

        gr.Markdown(BANNER)

        with gr.Row():

            with gr.Column(scale=3):

                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=430,
                )

                question = gr.Textbox(
                    label="Your question",
                    placeholder="e.g. Why are NSAIDs a concern in CKD?",
                    lines=2,
                    max_lines=4,
                )

                with gr.Row():
                    submit = gr.Button("Ask", variant="primary")
                    clear = gr.Button("Clear")

            with gr.Column(scale=2):
                metadata = gr.Markdown(
                    EMPTY_METADATA,
                    label="Response details"
                )

        gr.Examples(
            examples=EXAMPLES,
            inputs=question,
            label="Example questions (answerable from the demo corpus)",
        )

        gr.Markdown(
            "---\n"
            "Research prototype. The bundled corpus and drug records are **synthetic "
            "demo data**, contain no numeric doses, and are not validated medical "
            "sources. This system does not diagnose, does not recommend doses, and is "
            "not a substitute for a qualified clinician."
        )

        def respond(message: str, chat_history: list):

            chat_history = list(chat_history or [])
            query = (message or "").strip()

            if not query:
                return chat_history, gr.update(), ""

            answer, details = answer_query(query)

            chat_history.append((query, answer))

            return chat_history, details, ""

        submit.click(
            respond,
            [question, chatbot],
            [chatbot, metadata, question]
        )

        question.submit(
            respond,
            [question, chatbot],
            [chatbot, metadata, question]
        )

        clear.click(
            lambda: ([], EMPTY_METADATA, ""),
            None,
            [chatbot, metadata, question]
        )

    return demo
