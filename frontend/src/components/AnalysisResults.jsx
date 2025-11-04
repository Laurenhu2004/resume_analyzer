import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Heading,
  List,
  ListItem,
  ListIcon,
  Progress,
} from '@chakra-ui/react'
import { CheckCircleIcon } from '@chakra-ui/icons'

const AnalysisResults = ({ analysis }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'green'
    if (score >= 60) return 'yellow'
    return 'red'
  }

  return (
    <VStack spacing={6} align="stretch">
      {/* Score Badge */}
      <Box textAlign="center" py={4}>
        <Text fontSize="sm" color="gray.600" mb={2}>
          Overall Score
        </Text>
        <HStack justify="center" spacing={4}>
          <Badge
            fontSize="4xl"
            px={6}
            py={3}
            colorScheme={getScoreColor(analysis.score)}
            borderRadius="lg"
          >
            {analysis.score}/100
          </Badge>
          <Progress
            value={analysis.score}
            colorScheme={getScoreColor(analysis.score)}
            size="lg"
            width="200px"
            borderRadius="md"
          />
        </HStack>
      </Box>

      {/* Structure Feedback */}
      <Box borderWidth="1px" borderRadius="lg" p={6} bg="white" boxShadow="sm">
        <Heading size="md" mb={3}>
          Structure Feedback
        </Heading>
        <Text color="gray.700">{analysis.structure_feedback}</Text>
      </Box>

      {/* Keyword Analysis */}
      <Box borderWidth="1px" borderRadius="lg" p={6} bg="white" boxShadow="sm">
        <Heading size="md" mb={3}>
          Keyword Analysis
        </Heading>
        <Text color="gray.700">{analysis.keyword_analysis}</Text>
      </Box>

      {/* Improvements */}
      <Box borderWidth="1px" borderRadius="lg" p={6} bg="white" boxShadow="sm">
        <Heading size="md" mb={3}>
          Key Improvements
        </Heading>
        <List spacing={2}>
          {analysis.improvements.map((improvement, index) => (
            <ListItem key={index}>
              <ListIcon as={CheckCircleIcon} color="green.500" />
              {improvement}
            </ListItem>
          ))}
        </List>
      </Box>
    </VStack>
  )
}

export default AnalysisResults
