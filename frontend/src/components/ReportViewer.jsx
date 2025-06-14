import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Divider,
  Chip,
  Paper,
} from '@mui/material';

const ReportViewer = ({ report }) => {
  if (!report) return null;

  const renderSection = (section) => (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {section.title}
        </Typography>
        <Divider sx={{ mb: 2 }} />
        
        {/* Main Data */}
        <Grid container spacing={2}>
          {Object.entries(section.data).map(([key, value]) => (
            <Grid item xs={12} sm={6} key={key}>
              <Typography variant="subtitle2" color="text.secondary">
                {key.replace(/_/g, ' ').toUpperCase()}
              </Typography>
              <Typography variant="body1">{value}</Typography>
            </Grid>
          ))}
        </Grid>

        {/* Additional Info */}
        {Object.keys(section.additional_info).length > 0 && (
          <>
            <Typography variant="subtitle1" sx={{ mt: 2, mb: 1 }}>
              Additional Information
            </Typography>
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Grid container spacing={2}>
                {Object.entries(section.additional_info).map(([key, value]) => (
                  <Grid item xs={12} sm={6} key={key}>
                    <Typography variant="subtitle2" color="text.secondary">
                      {key.replace(/_/g, ' ').toUpperCase()}
                    </Typography>
                    <Typography variant="body2">{value}</Typography>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Box sx={{ p: 3 }}>
      {/* Report Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Lung Cancer Analysis Report
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Report ID: {report.report_id}
        </Typography>
        <Typography variant="subtitle2" color="text.secondary">
          Generated: {report.generated_at}
        </Typography>
      </Box>

      {/* Summary Section */}
      <Card sx={{ mb: 4, bgcolor: 'primary.light' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Summary
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {report.summary.key_findings.map((finding, index) => (
              <Chip
                key={index}
                label={finding}
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Main Sections */}
      {Object.entries(report.sections).map(([key, section]) => (
        <Box key={key}>
          {renderSection(section)}
        </Box>
      ))}
    </Box>
  );
};

export default ReportViewer; 