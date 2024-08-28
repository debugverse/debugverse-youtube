package main

import (
	"github.com/google/generative-ai-go/genai"
	"os"
	"path/filepath"
	"strings"
)

var fileWriteSchema = &genai.Schema{
	Type: genai.TypeObject,
	Properties: map[string]*genai.Schema{
		"fileName": {
			Type:        genai.TypeString,
			Description: "The name of the file to write to. Do not include extension, it will be automatically added (.txt)",
		},
		"content": {
			Type:        genai.TypeString,
			Description: "The text content to write to the file",
		},
	},
	Required: []string{"fileName", "content"},
}

var FileTool = &genai.Tool{
	FunctionDeclarations: []*genai.FunctionDeclaration{
		{
			Name:        "file_write",
			Description: "write a text file to user local file system with specified name and content.",
			Parameters:  fileWriteSchema,
		},
	},
}

func WriteDesktop(fileName string, content string) error {
	fileName = fileName + ".txt"
	home, _ := os.UserHomeDir()
	fullPath := filepath.Join(home, "Desktop", fileName)

	formattedContent := strings.ReplaceAll(content, "\\n", "\n")

	err := os.WriteFile(fullPath, []byte(formattedContent), 0644)
	if err != nil {
		return err
	}
	return nil
}
