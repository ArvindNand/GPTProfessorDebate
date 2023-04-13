import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Define a function to send prompts to the ChatGPT API
def ask_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Replace with the desired engine name
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_conversation(course_name, question, subject, loops):
    # Define the series of prompts
    start_prompts = [
        f"You are about to take on the role of Professor X. Professor X is a {subject} professor at a prestigious Ivy League Institution. You are teaching a course called {course_name}. I will take on the role of a student in this class. You have assigned a problem set and we are now in office hours. I will share the question with you and then you will teach me how to solve each problem. Unlike most students, I am not very smart, which means you need to take extra care when breaking down concepts. Fortunately, you are trained in advanced teaching pedagogies such as the Feynman Technique. Are you ready to take on the role of Professor X?",
        f"{question}",
        f"Professor X has now left the room. You are now going to take on the role of Professor Y. Professor Y is another professor at the same prestigious Ivy League institution. While Professor X often teaches the {course_name} course in the fall, Professor Y teaches the same {course_name} course in the spring. While you are good colleagues with Professor X, as Professor Y you do not always see things the same way and are well known for getting into arguments with Professor X over what the correct answer may be. I am still the same student in office hours, and now that Professor X is no longer in the room, I have asked you to provide your thoughts on the above response given by Professor X. Respond with your thoughts to Professor X's answer, and provide critique and corrections if you deem it necessary."
        "You are now going to take on the role of Professor X again. You have returned to the room and Professor Y is still present. As Professor X, respond to what Professor Y just said. State what you agree and disagree with and provide critique where necessary."
    ]

    loop_prompts = {
        "You are now going to take on the role of Professor Y again. You have listened to what Professor X just said and have prepared a rebuttal. As Professor Y, respond to what Professor X just said. State what you agree and disagree with and provide critique where necessary.",
        "You are now going to take on the role of Professor X again. You have listened to what Professor Y just said and have prepared a rebuttal. As Professor X, respond to what Professor Y just said. State what you agree and disagree with and provide critique where necessary."
    }

    synthesis_prompts = {
        "You are now going to take on the role of the student. You have listened to everything that has been said between Professor X and Professor Y. Based on all of Professor X and Professor Y's comments, come up with a more comprehensive answer to the original question: {question} Make sure to incorporate the best elements of everything that was said by Professor X and Professor Y.",
        "You will now take on the role of Professor X again. You have just seen the student's above response. Provide your feedback to the response, including any critiques and suggestions for improvement.", 
    }
    
    # Send each prompt to the ChatGPT API and print the response
    responses = []
    final_response = []
    for prompt in start_prompts:
        response = ask_chatgpt(prompt)
        responses.append(response)
    for i in range(loops):    
        for prompt in loop_prompts:
            response = ask_chatgpt(prompt)
            responses.append(response)    
    for prompt in synthesis_prompts:
        response = ask_chatgpt(prompt)
        responses.append(response)  
    response = ask_chatgpt("You will once again take on the role of the student. Incorporate Professor X's feedback into your original response.")
    responses.append(response)
    final_response.append(response)  

    # Combine the responses into a single text
    combined_responses = "\n".join(responses)  # Change this line to use a single newline character

    # Save the combined responses to a text file
    with open("combined_responses.txt", "w") as output_file:
        output_file.write(combined_responses)

    # Print the combined responses
    print(final_response)

def main():
    subject= input("Enter the subject: ")
    course_name = input("Enter the course name: ")
    question = input("Enter the question: ")
    loops = int(input("Enter the number of loops: "))
    generate_conversation(course_name, question, subject, loops)

if __name__ == "__main__":
    main()
