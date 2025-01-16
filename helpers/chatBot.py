import pytgpt.phind as phind


def get_gpt_output(input):
    bot = phind.PHIND()
    try:
        output = bot.chat(input)
    except:
        output = "Can not generate any output based on your input."
    return output