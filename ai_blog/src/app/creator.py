from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


async def create_blogpost(topic):
    blogprompt = (
        f"You are a professional blog wr iter. Write a 500-100 word SEO friendly, well structured, markdown-formatted blog post about the topic of {
            topic}. "
    )

    response_schemas = [
        ResponseSchema(
            name="blog title",
            description="SEO-friendly title of the blog post. Must not exceed 150 characters."
        ),
        ResponseSchema(
            name="post content",
            description="The content of the blog post. Do not include the title of the blog post again!"
        ),
        ResponseSchema(
            name="tags",
            description="List of relevant tags for the post, separated by comma. Maximum 5 tags."
        ),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas
    )
    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template="answer the users question as best as possible. \n {format_instructions} \n {question}",
        input_variables=["questions"],
        partial_variables={"format_instructions": format_instructions}

    )

    model = ChatOpenAI(model="gpt-4o", temperature=0.9)

    chain = prompt | model | output_parser

    try:
        response = await chain.ainvoke({"question": blogprompt})
    except Exception as e:
        print(str(e))
        return False, None

    result = {}
    result["tags"] = [tag.strip() for tag in response["tags"].split(",")]
    result["title"] = response["blog title"]
    result["content"] = response["post content"]

    return True, result
