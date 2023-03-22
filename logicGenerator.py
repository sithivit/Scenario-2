import openai


def get_questions(max_variable):
    openai.api_key = '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'

    messages = [
        {"role": "system",
         "content": f"Can you create 5 random solvable propositional logic expressions with each max {max_variable} variables using \/ for or /\ for and -> for imply ~ for not <=> for equivalent syntax."}
    ]

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})
    return reply, messages
