import google.generativeai as genai

def get_gemini_response(prompt: str, model: genai.GenerativeModel) -> str:
    """Calls the Gemini API with a pre-configured model and returns the text response."""
    response = model.generate_content(prompt)
    return response.text

def run_gemini_workflow(task: str, word_limit: int, api_key: str):
    """
    Orchestrates a precise, multi-step agent workflow using Google's Gemini model
    and your custom prompt formats.
    """
    # Configure the API and model only ONCE.
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    conversation_log = []

    # --- Define Agent Prompts using your format ---
    writer_prompt = f"""You are a professional blog post writer.
    Your only job is to write a first draft based on the provided topic.
    Make a note for the Final Editor that the post should be around {word_limit} words.
    Do not add any other commentary.
    Here is the topic:
    {task}"""

    seo_reviewer_prompt_template = """You are a professional SEO specialist. 
    Review the original draft below and provide your feedback 
    in three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**SEO Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""
    
    legal_reviewer_prompt_template = """You are a professional legal expert. 
    Review the original draft below for legal issues and provide your feedback
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Legal Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    ethics_reviewer_prompt_template = """You are a professional ethics expert. 
    Review the original draft below for ethical concerns and provide your feedback 
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Ethical Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    plagiarism_checker_prompt_template = """You are a professional plagiarism checker. 
    Check the original draft below for originality and provide your findings 
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Plagiarism Checker:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    final_editor_prompt_template = """You are the professional final editor. 
    Rewrite the original draft solely based on the consolidated feedback provided.
    The final rewritten draft should strictly match the word count of the original draft.
    Do not mention the word count in your draft. 
    Output two things, each clearly labeled: '--- ORIGINAL DRAFT ---' and '--- FINAL REWRITTEN DRAFT ---'.

    {consolidated_feedback}"""

    # --- Execute the Workflow Step-by-Step ---

    # Step 1: Writer creates the first draft
    original_draft = get_gemini_response(writer_prompt, model)
    conversation_log.append(f"\n{original_draft}")

    # Step 2: Get feedback from all reviewers
    seo_feedback = get_gemini_response(seo_reviewer_prompt_template.format(draft=original_draft), model)
    conversation_log.append(f"\n{seo_feedback}")

    legal_feedback = get_gemini_response(legal_reviewer_prompt_template.format(draft=original_draft), model)
    conversation_log.append(f"\n{legal_feedback}")

    ethics_feedback = get_gemini_response(ethics_reviewer_prompt_template.format(draft=original_draft), model)
    conversation_log.append(f"\n{ethics_feedback}")

    plagiarism_feedback = get_gemini_response(plagiarism_checker_prompt_template.format(draft=original_draft), model)
    conversation_log.append(f"\n{plagiarism_feedback}")

    # Step 3: Consolidate feedback and send to Final Editor
    consolidated_feedback = f"""
    \n--- ORIGINAL DRAFT ---\n
    \n{original_draft}\n

    \n--- CONSOLIDATED FEEDBACK ---\n
    \n{seo_feedback}\n

    \n{legal_feedback}\n

    \n{ethics_feedback}\n

    \n{plagiarism_feedback}\n
    """
    conversation_log.append(f"\n\n----------Consolidated Feedback for Editor----------\n\n{consolidated_feedback}")

    final_post_with_original = get_gemini_response(final_editor_prompt_template.format(consolidated_feedback=consolidated_feedback), model)
    conversation_log.append(f"\n\n----------Final Editor's Output----------\n\n{final_post_with_original}")

    # Extract only the final rewritten draft to display as the main result
    final_post = final_post_with_original.split("--- FINAL REWRITTEN DRAFT ---")[-1].strip()

    return final_post, "<br><br>".join(conversation_log)