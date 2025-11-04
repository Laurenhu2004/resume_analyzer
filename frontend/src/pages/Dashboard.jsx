import { useState } from 'react'
import {
  Container,
  Box,
  VStack,
  Heading,
  Button,
  useToast,
  Spinner,
  Center,
  Text,
  HStack,
} from '@chakra-ui/react'
import { authService } from '../services/authService'
import { resumeService } from '../services/resumeService'
import UploadZone from '../components/UploadZone'
import AnalysisResults from '../components/AnalysisResults'
import ImprovementSuggestions from '../components/ImprovementSuggestions'

const Dashboard = () => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const toast = useToast()

  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile)
    setAnalysis(null)
    setLoading(true)

    try {
      const result = await resumeService.uploadAndAnalyze(selectedFile)
      setAnalysis(result)
      toast({
        title: 'Success',
        description: 'Resume analyzed successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to analyze resume',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setAnalysis(null)
  }

  return (
    <Container maxW="6xl" py={8}>
      <VStack spacing={8} align="stretch">
        {/* Header */}
        <Box>
          <HStack justify="space-between" mb={4}>
            <Heading size="lg">Resume Analyzer</Heading>
            <Button
              variant="outline"
              onClick={() => authService.logout()}
            >
              Logout
            </Button>
          </HStack>
          <Text color="gray.600">
            Upload your resume to get AI-powered feedback and improvements
          </Text>
        </Box>

        {/* Upload Zone */}
        {!analysis && (
          <UploadZone onFileSelect={handleFileSelect} loading={loading} />
        )}

        {/* Loading State */}
        {loading && (
          <Center py={12}>
            <VStack spacing={4}>
              <Spinner size="xl" color="blue.500" />
              <Text color="gray.600">Analyzing your resume...</Text>
            </VStack>
          </Center>
        )}

        {/* Analysis Results */}
        {analysis && !loading && (
          <>
            <Button
              onClick={handleReset}
              variant="outline"
              alignSelf="flex-start"
            >
              Upload New Resume
            </Button>
            <AnalysisResults analysis={analysis} />
            <ImprovementSuggestions improvedContent={analysis.improved_content} />
          </>
        )}
      </VStack>
    </Container>
  )
}

export default Dashboard
