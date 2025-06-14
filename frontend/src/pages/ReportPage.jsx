import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import ReportViewer from '../components/ReportViewer';

const ReportPage = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [report, setReport] = useState(null);
  const [formData, setFormData] = useState({
    patient_info: {
      name: '',
      age: '',
      gender: '',
      additionalProp1: {
        occupation: '',
        medical_history: '',
      },
    },
    cancer_result: {
      prediction: '',
      confidence: '',
      additionalProp1: {
        stage: '',
        location: '',
      },
    },
    risk_analysis: {
      risk_level: '',
      recommendations: '',
      additionalProp1: {
        follow_up: '',
        specialist: '',
      },
    },
  });

  const handleInputChange = (section, field, value, isAdditional = false) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        ...(isAdditional
          ? {
              additionalProp1: {
                ...prev[section].additionalProp1,
                [field]: value,
              },
            }
          : { [field]: value }),
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate report');
      }

      const data = await response.json();
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Generate Cancer Analysis Report
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
          {/* Patient Information */}
          <Typography variant="h6" gutterBottom>
            Patient Information
          </Typography>
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
            <TextField
              label="Name"
              value={formData.patient_info.name}
              onChange={(e) => handleInputChange('patient_info', 'name', e.target.value)}
              required
            />
            <TextField
              label="Age"
              type="number"
              value={formData.patient_info.age}
              onChange={(e) => handleInputChange('patient_info', 'age', e.target.value)}
              required
            />
            <TextField
              label="Gender"
              value={formData.patient_info.gender}
              onChange={(e) => handleInputChange('patient_info', 'gender', e.target.value)}
              required
            />
            <TextField
              label="Occupation"
              value={formData.patient_info.additionalProp1.occupation}
              onChange={(e) => handleInputChange('patient_info', 'occupation', e.target.value, true)}
            />
            <TextField
              label="Medical History"
              value={formData.patient_info.additionalProp1.medical_history}
              onChange={(e) => handleInputChange('patient_info', 'medical_history', e.target.value, true)}
              multiline
              rows={2}
            />
          </Box>

          {/* Cancer Result */}
          <Typography variant="h6" sx={{ mt: 4 }} gutterBottom>
            Cancer Detection Result
          </Typography>
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
            <TextField
              label="Prediction"
              value={formData.cancer_result.prediction}
              onChange={(e) => handleInputChange('cancer_result', 'prediction', e.target.value)}
              required
            />
            <TextField
              label="Confidence"
              type="number"
              value={formData.cancer_result.confidence}
              onChange={(e) => handleInputChange('cancer_result', 'confidence', e.target.value)}
              required
            />
            <TextField
              label="Stage"
              value={formData.cancer_result.additionalProp1.stage}
              onChange={(e) => handleInputChange('cancer_result', 'stage', e.target.value, true)}
            />
            <TextField
              label="Location"
              value={formData.cancer_result.additionalProp1.location}
              onChange={(e) => handleInputChange('cancer_result', 'location', e.target.value, true)}
            />
          </Box>

          {/* Risk Analysis */}
          <Typography variant="h6" sx={{ mt: 4 }} gutterBottom>
            Risk Analysis
          </Typography>
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))' }}>
            <TextField
              label="Risk Level"
              value={formData.risk_analysis.risk_level}
              onChange={(e) => handleInputChange('risk_analysis', 'risk_level', e.target.value)}
            />
            <TextField
              label="Recommendations"
              value={formData.risk_analysis.recommendations}
              onChange={(e) => handleInputChange('risk_analysis', 'recommendations', e.target.value)}
              multiline
              rows={2}
            />
            <TextField
              label="Follow-up"
              value={formData.risk_analysis.additionalProp1.follow_up}
              onChange={(e) => handleInputChange('risk_analysis', 'follow_up', e.target.value, true)}
            />
            <TextField
              label="Specialist"
              value={formData.risk_analysis.additionalProp1.specialist}
              onChange={(e) => handleInputChange('risk_analysis', 'specialist', e.target.value, true)}
            />
          </Box>

          <Button
            type="submit"
            variant="contained"
            size="large"
            disabled={loading}
            sx={{ mt: 4 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Report'}
          </Button>
        </Box>

        {/* Report Display */}
        {report && <ReportViewer report={report} />}
      </Box>
    </Container>
  );
};

export default ReportPage; 