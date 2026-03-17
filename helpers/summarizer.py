import logging

logger = logging.getLogger(__name__)

def generate_summary_with_gpt(transcript, client):
    try:
        prompt = f"""
        Please provide a comprehensive summary of the following transcript. 
        Include key points, main topics discussed, and important details:

        {transcript}

        Summary:
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise and informative summaries from transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        return f"Error generating summary: {str(e)}"