import json
from abc import abstractmethod

import openai
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)


class LLM:
    @abstractmethod
    def completion(self, *args, **kwargs):
        """Generate text"""
        raise NotImplementedError

    @retry(
        wait=wait_random_exponential(min=1, max=20),
        stop=stop_after_attempt(3),
        retry=(
            retry_if_exception_type(openai.error.RateLimitError)
            | retry_if_exception_type(openai.error.ServiceUnavailableError)
        ),
    )
    def completion_with_retry(self, *args, **kwargs):
        return self.completion(*args, **kwargs)


class GPT(LLM):
    def __init__(
        self,
        model: str = "text-davinci-003",
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        logit_bias={},
    ):
        self.params = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "n": n,
            "logit_bias": logit_bias,
        }

    def completion(self, prompt):
        print("PROMPT: {prompt}".format(prompt=prompt))
        response = openai.Completion.create(prompt=prompt, **self.params)
        text = response.choices[0].text
        print("ANSWER: {answer}".format(answer=text))
        return text


class ChatGPT(LLM):
    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=None,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        logit_bias={},
    ):
        self.params = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "n": n,
            "logit_bias": logit_bias,
        }

    def completion(
        self, prompt, system_message="You are a helpful assistant.", history=None
    ):
        messages = []
        if history:
            messages.extend(history)
        elif system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        print("MESSAGES: {messages}".format(messages=json.dumps(messages, indent=4)))
        response = openai.ChatCompletion.create(messages=messages, **self.params)
        text = response.choices[0].message["content"]
        print("ANSWER: {answer}".format(answer=text))
        return text
