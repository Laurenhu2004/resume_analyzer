import { useState, useEffect } from 'react'
import {
  Box,
  Textarea,
  Button,
  VStack,
  Heading,
  Text,
  useToast,
} from '@chakra-ui/react'
import { resumeService } from '../services/resumeService'

const ImprovementSuggestions = ({ improvedContent }) => {
  const [content, setContent] = useState(improvedContent)
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  useEffect(() => {
    setContent(improvedContent)
  }, [improvedContent])

  const handleExport = async () => {
    setLoading(true)
    try {
      await resumeService.exportImprovedResume(content)
      toast({
        title: 'Success',
        description: 'Resume PDF downloaded successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to export resume',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <VStack spacing={4} align="stretch">
      <Box>
        <Heading size="md" mb={2}>
          Improved Resume
        </Heading>
        <Text color="gray.600" mb={4}>
          Review and edit the improved resume below, then export as PDF
        </Text>
      </Box>
      <Textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Improved resume content will appear here..."
        minH="400px"
        fontFamily="mono"
        fontSize="sm"
      />
      <Button
        colorScheme="blue"
        onClick={handleExport}
        isLoading={loading}
        loadingText="Generating PDF..."
        size="lg"
      >
        Export as PDF
      </Button>
    </VStack>
  )
}

export default ImprovementSuggestions
