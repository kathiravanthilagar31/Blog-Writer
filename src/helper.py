import google.generativeai as genai

def get_gemini_response(prompt: str, model: genai.GenerativeModel) -> str:
    """Calls the Gemini API with a pre-configured model and returns the text response."""
    response = model.generate_content(prompt)
    return response.text

def run_review_process(draft: str, model: genai.GenerativeModel, log_callback):
    """
    This function simulates a nested chat for the review process.
    It gathers feedback from all reviewers and then consolidates it.
    """
    # --- Define Reviewer Prompts ---
    seo_reviewer_prompt = f"""You are a professional SEO specialist. 
    Review the original draft below and provide your feedback 
    in three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**SEO Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""
    
    legal_reviewer_prompt = f"""You are a professional legal expert. 
    Review the original draft below for legal issues and provide your feedback
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Legal Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    ethics_reviewer_prompt = f"""You are a professional ethics expert. 
    Review the original draft below for ethical concerns and provide your feedback 
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Ethical Reviewer:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    plagiarism_checker_prompt = f"""You are a professional plagiarism checker. 
    Check the original draft below for originality and provide your findings 
    in up to three separate, ordered bullet lines that start with ➡️.
    Do not use numbered points.
    Start your feedback with the bolded header '**Plagiarism Checker:**'.

    --- ORIGINAL DRAFT ---
    {draft}"""

    # --- Get Individual Feedback ---
    seo_feedback = get_gemini_response(seo_reviewer_prompt, model)
    log_callback(f"\n{seo_feedback}")

    legal_feedback = get_gemini_response(legal_reviewer_prompt, model)
    log_callback(f"\n{legal_feedback}")

    ethics_feedback = get_gemini_response(ethics_reviewer_prompt, model)
    log_callback(f"\n{ethics_feedback}")

    plagiarism_feedback = get_gemini_response(plagiarism_checker_prompt, model)
    log_callback(f"\n{plagiarism_feedback}")

    # --- The "Review Manager" consolidates the feedback ---
    consolidation_prompt = f"""You are a review manager. Your job is to combine the following feedback points into a single, clean, consolidated report.

    --- FEEDBACKS ---
    {seo_feedback}
    {legal_feedback}
    {ethics_feedback}
    {plagiarism_feedback}
    """
    consolidated_feedback = get_gemini_response(consolidation_prompt, model)
    
    return consolidated_feedback


def run_gemini_workflow(task: str, word_limit: int, api_key: str):
    """
    Orchestrates the main workflow, delegating the review process to a nested function.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    conversation_log = []
    def log_message(message):
        conversation_log.append(message)

    # --- Define Main Agent Prompts ---
    writer_prompt = f"""You are a professional blog post writer.
    Your only job is to write a first draft based on the provided topic.
    Make a note for the Final Editor that the post should be around {word_limit} words.
    Do not add any other commentary.
    Here is the topic:
    {task}"""

    final_editor_prompt_template = """You are the professional final editor. 
    Rewrite the original draft solely based on the consolidated feedback provided.
    The final rewritten draft should strictly match the word count of the original draft.
    Do not mention the word count in your draft. 
    Output two things, each clearly labeled: '--- ORIGINAL DRAFT ---' and '--- FINAL REWRITTEN DRAFT ---'.

    --- ORIGINAL DRAFT ---
    {original_draft}

    --- CONSOLIDATED FEEDBACK ---
    {consolidated_feedback}"""

    # --- Execute the Main Workflow ---

    # Step 1: Writer creates the first draft
    original_draft = get_gemini_response(writer_prompt, model)
    log_message(f"\n--------------- FIRST DRAFT ----------------\n\n{original_draft}")

    # Step 2: Delegate the entire review process to the nested function
    consolidated_feedback = run_review_process(original_draft, model, log_message)
    log_message(f"\n\n----------Consolidated Feedback for Editor----------\n\n{consolidated_feedback}")

    # Step 3: Send the consolidated feedback to the Final Editor
    final_editor_prompt = final_editor_prompt_template.format(
        original_draft=original_draft,
        consolidated_feedback=consolidated_feedback
    )
    final_post_with_original = get_gemini_response(final_editor_prompt, model)
    log_message(f"\n\n----------Final Editor's Output----------\n\n{final_post_with_original}")

    # Extract only the final rewritten draft to display as the main result
    final_post = final_post_with_original.split("--- FINAL REWRITTEN DRAFT ---")[-1].strip()

    return final_post, "<br><br>".join(conversation_log)