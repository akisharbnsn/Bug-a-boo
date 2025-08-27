#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openai import OpenAI

client = OpenAI()

def get_hint_from_llm(code: str, tier: int) -> str:
    """
    Send buggy code to the LLM and ask for a tiered hint.
    """
    system_prompt = """
    You are a debugging assistant. 
    A user will give you buggy Python code. 
    You will give tiered hints instead of the final solution:
      - Tier 1: Very general hint (point in the right direction)
      - Tier 2: More specific hint (narrow down likely bug area)
      - Tier 3: Very detailed guidance
      - Tier 4: Provide corrected working code
    Do not jump ahead to higher tiers unless requested.
    """

    user_prompt = f"""
    The user has provided this buggy Python code:

    {code}

    Please provide the Tier {tier} hint only.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content


# In[ ]:


def interactive_debug():
    print("Welcome to the interactive debugging assistant!")
    print("Enter your buggy Python code (end with a blank line):")

    # Read multiline input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    buggy_code = "\n".join(lines)

    for tier in range(1, 5):
        hint = get_hint_from_llm(buggy_code, tier)
        print(f"\nTier {tier} Hint:\n{hint}\n")
        if tier < 4:
            cont = input("Do you want to see the next tier hint? (y/n): ")
            if cont.lower() != 'y':
                break

if __name__ == "__main__":
    interactive_debug()

