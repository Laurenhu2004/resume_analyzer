import { useRef, useState } from 'react'
import {
  Box,
  Button,
  VStack,
  Text,
  useColorModeValue,
  Icon,
} from '@chakra-ui/react'

const UploadZone = ({ onFileSelect, loading }) => {
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef(null)
  const borderColor = useColorModeValue('gray.300', 'gray.600')
  const bgColor = useColorModeValue('gray.50', 'gray.700')
  const dragBgColor = useColorModeValue('blue.50', 'blue.900')

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files.length > 0 && files[0].type === 'application/pdf') {
      onFileSelect(files[0])
    }
  }

  const handleFileInput = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      onFileSelect(files[0])
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <Box
      borderWidth="2px"
      borderStyle="dashed"
      borderColor={isDragging ? 'blue.500' : borderColor}
      borderRadius="lg"
      p={12}
      textAlign="center"
      bg={isDragging ? dragBgColor : bgColor}
      cursor="pointer"
      transition="all 0.2s"
      _hover={{
        borderColor: 'blue.400',
        bg: dragBgColor,
      }}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf"
        onChange={handleFileInput}
        style={{ display: 'none' }}
        disabled={loading}
      />
      <VStack spacing={4}>
        <Icon boxSize={12} color="blue.500">
          <svg
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </Icon>
        <Text fontSize="xl" fontWeight="bold">
          Drop your resume PDF here
        </Text>
        <Text color="gray.500">or click to browse</Text>
        <Text fontSize="sm" color="gray.400">
          Only PDF files are supported (max 5MB)
        </Text>
        <Button
          colorScheme="blue"
          isLoading={loading}
          loadingText="Uploading..."
          size="lg"
        >
          {loading ? 'Uploading...' : 'Select File'}
        </Button>
      </VStack>
    </Box>
  )
}

export default UploadZone
