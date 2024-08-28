package main

import (
	"context"
	"github.com/google/generative-ai-go/genai"
	"google.golang.org/api/option"
)

// NewClient return new genAI client
func NewClient(apiKey string, ctx context.Context) (*genai.Client, error) {
	client, err := genai.NewClient(ctx, option.WithAPIKey(apiKey))
	if err != nil {
		return nil, err
	}
	return client, nil
}

// NewModel return new generative model
func NewModel(client *genai.Client, model string) *genai.GenerativeModel {
	genaimodel := client.GenerativeModel(model)
	genaimodel.SafetySettings = []*genai.SafetySetting{
		{
			Category:  genai.HarmCategoryHarassment,
			Threshold: genai.HarmBlockNone,
		},
		{
			Category:  genai.HarmCategoryHateSpeech,
			Threshold: genai.HarmBlockNone,
		},
		{
			Category:  genai.HarmCategorySexuallyExplicit,
			Threshold: genai.HarmBlockNone,
		},
	}
	return genaimodel
}
