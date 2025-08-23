import autogen

# --- MONKEY PATCH TO FIX INCOMPATIBILITY (Keep this at the top) ---
import openai
from openai._base_client import SyncHttpxClientWrapper

class CustomHttpxClientWrapper(SyncHttpxClientWrapper):
    def __init__(self, *args, **kwargs):
        kwargs.pop("proxies", None)
        super().__init__(*args, **kwargs)

openai._base_client.SyncHttpxClientWrapper = CustomHttpxClientWrapper
# --- END OF PATCH ---


def run_autogen_workflow(task: str, config_list: list):
    """
    Orchestrates a precise, multi-step agent workflow and logs the conversation.
    """
    llm_config = {"config_list": config_list, "temperature": 0.7}
    conversation_log = []

    # --- Define All Agents ---
    user_proxy = autogen.UserProxyAgent(name="User_Proxy", code_execution_config=False, human_input_mode="NEVER")
    writer = autogen.AssistantAgent(name="Draft_Writer", llm_config=llm_config, 
                                    system_message="""You are a professional blog post writer.
                                    Your only job is to write a first draft based on the provided topic.
                                    Make a note for Final Editor about {Word_limit} 
                                    Do not add any other commentary.""")
    
    seo_reviewer = autogen.AssistantAgent(name="SEO_Reviewer", llm_config=llm_config, 
                                          system_message="""You are a professional SEO specialist. 
                                          Review the original draft and you should provide your feedback 
                                          starts with ordered,seperated bullet lines start with ➡️ not more than 3 points. 
                                          (e.g:)
                                          ➡️ point 1 content`\n`
                                          ➡️ point 2 content`\n`
                                          and so on.(But do not explicitly say like point 1, point 2)
                                          Start your feedback with the bolded header 'SEO Reviewer:'.""")
    
    legal_reviewer = autogen.AssistantAgent(name="Legal_Reviewer", llm_config=llm_config, 
                                            system_message="""You are a professional legal expert. 
                                            Review the original draft for legal issues and you should your provide feedback
                                            starts with ordered,seperated bullet lines start with ➡️ not more than 3 points.
                                            (e.g:)
                                            ➡️ point 1 content`\n`
                                            ➡️ point 2 content`\n`
                                            and so on.(But do not explicitly say like point 1, point 2)
                                            Start your feedback with the bolded header 'Legal Reviwer:'.""")
    
    ethics_reviewer = autogen.AssistantAgent(name="Ethics_Reviewer", llm_config=llm_config, 
                                             system_message="""You are a professional ethics expert. 
                                             Review the original draft for ethical concerns and you should your provide feedback 
                                             starts with ordered,seperated bullet lines start with ➡️ not more than 3 points 
                                             (e.g:)
                                             ➡️ point 1 content`\n`
                                             ➡️ point 2 content`\n`
                                             and so on.(But do not explicitly say like point 1, point 2)
                                             Start your feedback with the bolded header 'Ethical Reviewer:'.""")
    
    plagiarism_checker = autogen.AssistantAgent(name="Plagiarism_Checker", llm_config=llm_config, 
                                                system_message="""You are a professional plagiarism checker. 
                                                Check the original draft for plagiarism, originality and you should provide your findings 
                                                starts with ordered,seperated bullet lines start with ➡️ not more than 3 points 
                                                (e.g:)
                                                ➡️ point 1 content`\n`
                                                ➡️ point 2 content`\n`
                                                and so on.(But do not explicitly say like point 1, point 2)                                             
                                                Start your feedback with the bolded header 'Plagiarism Checker:'.""")
    
    final_editor = autogen.AssistantAgent(name="Final_Editor", llm_config=llm_config, 
                                          system_message=f"""You are the professional final editor. 
                                          Rewrite the original draft solely based on the consolidated feedback provided without any additional comments and 
                                          your rewritten '--- FINAL DRAFT ---' should and strictly match the count of number of words in '--- ORIGINAL DRAFT ---'.
                                          You should not mention note on word count in your draft. 
                                          Output two things, each clearly labeled: '--- ORIGINAL DRAFT ---' and '--- FINAL REWRITTEN DRAFT ---'.""")
    

    # --- Execute the Workflow Step-by-Step ---

    # Step 1: Writer creates the first draft
    chat_result_writer = user_proxy.initiate_chat(recipient=writer, message=task, max_turns=1, silent=False)
    original_draft = chat_result_writer.chat_history[-1]["content"]
    conversation_log.append(f"--------------- FIRST DRAFT ----------------\n\n{original_draft}")

    # Step 2: Get feedback from all reviewers
    review_task = f"Here is the draft to review:\n\n{original_draft}"
    
    chat_result_seo = user_proxy.initiate_chat(recipient=seo_reviewer, message=review_task, max_turns=1, silent=False)
    seo_feedback = chat_result_seo.chat_history[-1]["content"]
    conversation_log.append(f"{seo_feedback}")

    chat_result_legal = user_proxy.initiate_chat(recipient=legal_reviewer, message=review_task, max_turns=1, silent=False)
    legal_feedback = chat_result_legal.chat_history[-1]["content"]
    conversation_log.append(f"{legal_feedback}")

    chat_result_ethics = user_proxy.initiate_chat(recipient=ethics_reviewer, message=review_task, max_turns=1, silent=False)
    ethics_feedback = chat_result_ethics.chat_history[-1]["content"]
    conversation_log.append(f"{ethics_feedback}")

    chat_result_plagiarism = user_proxy.initiate_chat(recipient=plagiarism_checker, message=review_task, max_turns=1, silent=False)
    plagiarism_feedback = chat_result_plagiarism.chat_history[-1]["content"]
    conversation_log.append(f"{plagiarism_feedback}")

    # Step 3: Consolidate feedback and send to Final Editor
    consolidated_feedback =f"""
    
    \n\nPlease rewrite the following original draft based on the feedback provided.\n\n

    \n--- ORIGINAL DRAFT ---\n\n
    \n{original_draft}\n\n

    \n--- CONSOLIDATED FEEDBACK ---\n\n
    \n{seo_feedback}\n
    \n{legal_feedback}\n
    \n{ethics_feedback}\n
    \n{plagiarism_feedback}\n
    """
    
    conversation_log.append(f"\n---------- Consolidated Feedback for Editor ----------\n{consolidated_feedback}\n")

    chat_result_final = user_proxy.initiate_chat(recipient=final_editor, message=consolidated_feedback, max_turns=1, silent=False)
    final_post_with_original = chat_result_final.chat_history[-1]["content"]
    conversation_log.append(f"\n---------- Final Editor's Output ----------\n\n{final_post_with_original}\n")

    # Extract only the final rewritten draft to display as the main result
    final_post = final_post_with_original.split("--- FINAL REWRITTEN DRAFT ---")[-1].strip()

    return final_post, "<br><br>".join(conversation_log)