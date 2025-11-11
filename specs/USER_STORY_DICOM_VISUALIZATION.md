# User Story: DICOM Medical Imaging Visualization

**Date:** 2025-11-06  
**User Story:** "As Beabadoo, I can view DICOM data files and request searches of medical imaging repositories"

---

## Summary

Enable Beabadoo to visualize DICOM medical imaging data in 3D/VR and use AI agents to search open-source medical imaging repositories like The Cancer Imaging Archive (TCIA), finding relevant diagnostic images and scans.

## User Story

> **As Beabadoo**, I want to view DICOM medical imaging files in 3D/VR and ask agents to search medical imaging repositories, so I can analyze diagnostic images alongside scientific papers for comprehensive medical research.

## Example Use Cases

### Viewing DICOM Files
- "Load this CT scan and show it in 3D"
- "Display this MRI series with volume rendering"
- "Show me slice-by-slice view of this brain scan"
- "Compare these two X-rays side by side"
- "View this ultrasound in VR with measurement tools"

### Searching Medical Imaging Repositories
- "Find CT scans of lung cancer patients"
- "Show me brain MRIs with glioblastoma"
- "Search for breast cancer mammography images"
- "Get PET scans from melanoma studies"
- "Find cardiac CT scans with annotations"

### Combined Research Workflow
- "Find papers about lung cancer treatment AND CT scans from TCIA"
- "Show me the imaging data referenced in this paper"
- "Compare imaging protocols across different studies"

---

## DICOM Standard Overview

**DICOM (Digital Imaging and Communications in Medicine)**
- Website: https://www.dicomstandard.org/
- Standard for medical imaging data
- Includes metadata (patient info, acquisition parameters, etc.)
- Supports multiple modalities: CT, MRI, X-Ray, Ultrasound, PET, etc.

**Common DICOM Tags:**
- Patient demographics (anonymized)
- Study/Series information
- Image dimensions and spacing
- Acquisition parameters
- Equipment details

---

## Medical Imaging Repositories

### The Cancer Imaging Archive (TCIA)
- **URL:** https://www.cancerimagingarchive.net/
- **Content:** 200+ imaging collections, >60 million images
- **Modalities:** CT, MRI, PET, X-Ray, Pathology
- **REST API:** Available for programmatic access
- **Data:** Linked to clinical outcomes and genomic data

### Other Open Repositories
1. **NIH Medical Imaging Commons**
   - Multi-institutional imaging data
   - Federated search across repositories

2. **OpenNeuro** (neuroimaging)
   - Brain MRI and fMRI datasets
   - BIDS format (compatible with DICOM)

3. **UK Biobank** (restricted access)
   - Large-scale population imaging
   - Multi-organ MRI data

4. **MIMIC-CXR** (chest X-rays)
   - 377,000+ chest X-ray images
   - Linked to electronic health records

---

## Technical Requirements

### 1. DICOM File Support

#### Backend (Python)
```python
# Required libraries
- pydicom: Parse DICOM files
- SimpleITK / itk: Medical image processing
- numpy: Array manipulation
- pillow: Image conversion
```

**Tasks:**
- Parse DICOM files and extract metadata
- Support multi-slice series (CT, MRI)
- Convert DICOM to web-friendly formats (PNG, JPG for 2D; NIfTI for 3D)
- Handle different modalities (CT, MRI, X-Ray, etc.)
- Anonymize patient data (remove PHI)
- Extract acquisition parameters

**Endpoints:**
```
POST   /api/v1/dicom/upload          # Upload DICOM files
GET    /api/v1/dicom/{id}            # Get DICOM metadata
GET    /api/v1/dicom/{id}/image      # Get image data
GET    /api/v1/dicom/{id}/series     # Get series information
GET    /api/v1/dicom/studies         # List all studies
POST   /api/v1/dicom/anonymize       # Anonymize DICOM data
```

#### Frontend (BabylonJS)

**2D Slice Viewer:**
- Display individual DICOM slices
- Windowing/Leveling controls (adjust brightness/contrast)
- Pan/zoom/rotate
- Measurement tools (distance, angle, area)
- Multi-planar reconstruction (MPR)

**3D Volume Rendering:**
- Volume rendering for CT/MRI series
- Adjustable transfer functions (opacity, color)
- Clipping planes
- Isosurface extraction
- Maximum Intensity Projection (MIP)

**VR/XR Features:**
- Immersive 3D volume viewing
- Gesture-based slice navigation
- Spatial measurement tools
- Multi-modal overlay (CT + PET)

### 2. Medical Imaging Repository Search

#### Research Agent Enhancement

**New Capabilities:**
- Query TCIA REST API (v3 and v4)
- Parse TCIA collection metadata
- Filter by modality, body part, disease
- Download image series metadata
- Link images to publications
- Use RAG to query Awesome DICOM resources for best practices

**TCIA API Integration:**
```python
# TCIA REST API v4 endpoints (preferred)
# API Documentation: https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides

GET /v4/query/getCollectionValues      # List collections
GET /v4/query/getModalityValues        # List modalities  
GET /v4/query/getBodyPartValues        # List body parts
GET /v4/query/getPatientStudy          # Get study info
GET /v4/query/getSeries                # Get series info
GET /v4/query/getImage                 # Download image
GET /v4/query/getSOPInstanceUIDs       # Get DICOM instance UIDs
```

**Awesome DICOM Knowledge Base:**
- Index the awesome-dicom repository for RAG
- Provides curated information on:
  - DICOM libraries (Python, JavaScript, C++)
  - DICOM viewers and tools
  - Sample datasets
  - Implementation guides
  - Best practices
  - Open-source projects
- Agent can reference when answering DICOM-related questions

**Search Parameters:**
- Collection name (e.g., "TCGA-LUAD" for lung cancer)
- Modality (CT, MRI, PET, etc.)
- Body part examined
- Manufacturer
- Study date range

#### Agent Query Processing

**Natural Language Examples:**
```
"Find CT scans of lung nodules"
→ Collection: LIDC-IDRI
→ Modality: CT
→ Body Part: Chest

"Show me glioblastoma MRIs with survival data"
→ Collection: TCGA-GBM
→ Modality: MRI
→ Include: Clinical data

"Get breast cancer mammography from 2020-2023"
→ Collection: CBIS-DDSM
→ Modality: MG (Mammography)
→ Date Range: 2020-2023
```

**Endpoints:**
```
POST   /api/v1/agents/search/imaging           # Search medical images
GET    /api/v1/agents/search/imaging/{task_id} # Get search results
POST   /api/v1/agents/download/imaging         # Download image series
GET    /api/v1/imaging/collections             # List available collections
```

### 3. Integrated Workflow

**Scenario:** Research lung cancer imaging
1. Beabadoo asks: "Find papers about lung nodule detection"
2. Agent returns relevant papers
3. Beabadoo asks: "Show me CT scans with lung nodules"
4. Agent searches TCIA for LIDC-IDRI collection
5. Returns preview images with metadata
6. Beabadoo selects a series
7. Agent downloads DICOM files
8. Client displays 3D volume rendering in VR
9. Beabadoo can annotate findings
10. Results saved alongside paper references

---

## Implementation Plan

### Phase 1: DICOM File Viewer (Backend)
**Time Estimate:** 8-12 hours

**Tasks:**
1. Install pydicom, SimpleITK
2. Create DICOM parser service
3. Implement DICOM upload endpoint
4. Extract metadata and store in database
5. Convert DICOM to PNG/JPG for preview
6. Support multi-slice series
7. Implement anonymization
8. Create DICOM REST endpoints
9. Add tests for DICOM parsing

**Files to Create:**
- `server/app/services/dicom_service.py`
- `server/app/api/routes/dicom.py`
- `server/app/models/dicom.py`
- `server/tests/test_dicom_service.py`

### Phase 2: DICOM Visualization (Frontend)
**Time Estimate:** 12-16 hours

**Tasks:**
1. Research DICOM viewers for web (e.g., Cornerstone.js, AMI.js)
2. Integrate DICOM viewer library
3. Create DicomViewer component (2D slices)
4. Implement windowing/leveling controls
5. Add measurement tools
6. Create Volume3D component (3D rendering)
7. Implement VR controls for navigation
8. Add multi-planar reconstruction
9. Test with sample DICOM files

**Files to Create:**
- `client/src/components/dicom/DicomViewer.tsx`
- `client/src/components/dicom/Volume3D.tsx`
- `client/src/components/dicom/DicomControls.tsx`
- `client/src/lib/dicom/dicomLoader.ts`
- `client/src/lib/dicom/volumeRenderer.ts`

**Libraries to Consider:**
- **Cornerstone.js** - 2D DICOM viewer (medical-grade)
- **AMI.js** - 3D medical imaging (BabylonJS compatible)
- **vtk.js** - 3D visualization toolkit
- **OHIF Viewer** - Full-featured DICOM viewer (heavy)

### Phase 3: TCIA Integration (Backend)
**Time Estimate:** 10-14 hours

**Tasks:**
1. Create TCIA API v4 client (REST)
2. Implement search by collection/modality/body part
3. Enhance Research Agent for imaging queries
4. Add NLP processing for imaging-related queries
5. Index Awesome DICOM repository into vector DB for RAG
6. Enable agent to query DICOM knowledge base
7. Create endpoints for imaging search
8. Implement background download of DICOM series
9. Store TCIA metadata in database
10. Link imaging data to papers
11. Add tests for TCIA integration

**Files to Create:**
- `server/app/services/tcia_client.py` (TCIA API v4 client)
- `server/app/agents/imaging_agent.py` (with RAG support)
- `server/app/api/routes/imaging_search.py`
- `server/data/knowledge_bases/awesome_dicom.md` (indexed for RAG)
- `server/tests/test_tcia_integration.py`

### Phase 4: Imaging Search UI (Frontend)
**Time Estimate:** 8-12 hours

**Tasks:**
1. Create ImagingSearchBar component
2. Add modality/body part filters
3. Create ImagingResults component
4. Display preview thumbnails
5. Show DICOM metadata
6. Implement download/view workflow
7. Integrate with 3D scene
8. Add VR voice search for imaging
9. Test end-to-end workflow

**Files to Create:**
- `client/src/components/imaging/ImagingSearchBar.tsx`
- `client/src/components/imaging/ImagingResults.tsx`
- `client/src/components/imaging/ImagingPreview.tsx`
- `client/src/lib/api/imaging.ts`
- `client/src/lib/hooks/useImagingSearch.ts`

---

## New GitHub Issue

### Issue #39: DICOM Medical Imaging Support

**Priority:** P2 (Medium) - Advanced feature  
**Time Estimate:** 38-54 hours (Backend: 18-26, Frontend: 20-28)  
**Phase:** Phase 3 - Advanced Features

**Description:**

Enable viewing DICOM medical imaging files and searching medical imaging repositories like The Cancer Imaging Archive (TCIA).

**User Story:**

As Beabadoo, I want to view DICOM medical images and search open-source imaging repositories, so I can analyze diagnostic images alongside scientific papers.

**Technical Components:**

1. **DICOM File Support (8-12 hrs)**
   - Parse DICOM files with pydicom
   - Extract metadata and anonymize
   - Convert to web formats
   - Create REST endpoints

2. **DICOM Visualization (12-16 hrs)**
   - 2D slice viewer with windowing
   - 3D volume rendering
   - VR/XR support
   - Measurement tools

3. **TCIA Integration (10-14 hrs)**
   - TCIA API client
   - Search by modality/body part/disease
   - Download DICOM series
   - Link to papers

4. **Imaging Search UI (8-12 hrs)**
   - Natural language search
   - Preview thumbnails
   - Metadata display
   - VR voice search

**Dependencies:**
- Issue #10 (Agents) - Research Agent enhancement
- Issue #32 (Document API) - Similar patterns
- Issue #38 (Agent Search) - Search infrastructure

**Deliverables:**
- DICOM file upload and viewing
- 3D volume rendering in VR
- TCIA repository search
- Integrated medical research workflow

**Related Links:**
- DICOM Standard: https://www.dicomstandard.org/
- TCIA: https://www.cancerimagingarchive.net/
- TCIA REST API Documentation: https://wiki.cancerimagingarchive.net/display/Public/TCIA+Programmatic+Interface+REST+API+Guides
- Awesome DICOM Resources: https://github.com/open-dicom/awesome-dicom

---

## Success Metrics

- [ ] Can upload and view DICOM files
- [ ] 2D slice viewer with windowing works
- [ ] 3D volume rendering displays correctly
- [ ] Can search TCIA by modality and body part
- [ ] Agent understands imaging-related queries
- [ ] VR volume viewing is smooth (>60 FPS)
- [ ] DICOM anonymization removes PHI
- [ ] Measurement tools are accurate
- [ ] Can link images to related papers

---

## Future Enhancements

### Advanced Features
- **DICOM-RT support** - Radiation therapy structures
- **DICOM-SR support** - Structured reports
- **AI-assisted annotations** - Auto-detect lesions
- **Image registration** - Align multi-modal images
- **4D imaging** - Time-series visualization
- **Quantitative analysis** - Volume calculations, SUV for PET

### Additional Repositories
- **NIH Medical Imaging Commons**
- **OpenNeuro** (brain imaging)
- **MIMIC-CXR** (chest X-rays)
- **UK Biobank** (population imaging)

### Clinical Integration
- **PACS integration** - Connect to hospital systems
- **HL7 FHIR** - Standard clinical data exchange
- **Multi-user annotation** - Collaborative diagnosis
- **Teaching files** - Educational collections

### Research Tools
- **Radiomics** - Extract quantitative features
- **Machine learning** - Train models on imaging data
- **Statistical analysis** - Survival curves, correlations
- **Publication figures** - Export high-quality images

---

## Privacy & Compliance Considerations

### HIPAA Compliance (if using patient data)
- **De-identification:** Remove all 18 PHI identifiers
- **Access controls:** User authentication and authorization
- **Audit logs:** Track all data access
- **Encryption:** At rest and in transit
- **Business Associate Agreements:** With repository providers

### TCIA Data Use
- **Open access:** Most TCIA data is de-identified and public
- **Attribution:** Cite collection creators in publications
- **Data Use Agreements:** May be required for some collections
- **No redistribution:** Don't re-host TCIA data

### Best Practices
- **Anonymize before upload:** Remove PHI client-side
- **Secure storage:** Encrypted database
- **Limited retention:** Delete data after analysis
- **User training:** HIPAA awareness for all users

---

## Testing Strategy

### Sample DICOM Files
1. **TCIA Sample Data:** Download small series for testing
2. **DICOM Test Files:** Use standard test datasets
3. **Multiple Modalities:** CT, MRI, X-Ray, PET
4. **Edge Cases:** Large series, unusual metadata

### Integration Tests
- Upload DICOM file → Parse → Store → Retrieve
- Search TCIA → Display results → Download → View
- Natural language query → Agent search → Display images
- Volume rendering → VR view → Measurements

### Performance Tests
- Large DICOM series (500+ slices)
- Multiple concurrent viewers
- VR frame rate (target: 60+ FPS)
- Network bandwidth (streaming large files)

---

## Documentation Needs

### User Documentation
- **DICOM User Guide:** How to upload and view files
- **TCIA Search Guide:** How to find medical images
- **VR Controls:** Navigating 3D volumes
- **Measurement Tools:** How to use annotations

### Developer Documentation
- **DICOM API Reference:** Endpoints and schemas
- **TCIA Integration:** API client usage
- **Viewer Components:** Props and customization
- **Privacy Guidelines:** Handling medical data

---

## Cost & Resource Considerations

### Storage
- DICOM files are large (CT series: 50-500 MB)
- Need adequate storage for temporary downloads
- Consider S3/cloud storage for production

### Compute
- Volume rendering is GPU-intensive
- 3D reconstruction requires processing power
- May need dedicated GPU instances

### Bandwidth
- TCIA downloads can be large
- Consider caching frequently accessed series
- Implement progressive loading for large files

### API Limits
- TCIA API has rate limits
- Implement request queuing
- Cache collection metadata

---

## Impact on Project Architecture

### New Services
- **DICOMService:** Parse and process medical images
- **TCIAClient:** Interface to Cancer Imaging Archive
- **ImagingAgent:** Specialized agent for medical imaging

### Database Schema
```sql
-- New tables
dicom_studies (id, patient_id, study_date, modality, ...)
dicom_series (id, study_id, series_number, images_count, ...)
dicom_images (id, series_id, instance_number, file_path, ...)
imaging_collections (id, name, repository, modality, ...)
imaging_searches (id, user_id, query, results, timestamp)
```

### Vector DB Integration
- Index DICOM metadata for semantic search
- Link imaging data to papers by keywords
- Search by anatomical regions and findings
- **Index Awesome DICOM repository** for RAG queries
  - DICOM libraries and tools knowledge
  - Implementation best practices
  - Sample datasets references
  - Enable agent to answer: "What's the best Python library for DICOM parsing?"

### Event Bus
- `imaging.upload.started`
- `imaging.upload.completed`
- `imaging.search.started`
- `imaging.search.completed`
- `imaging.download.progress`

---

## Timeline

**Phase 3 - Advanced Features** (After basic client integration complete)

### Week 1: DICOM Backend
- Day 1-2: Set up pydicom, implement parser
- Day 3-4: Create REST endpoints
- Day 5: Testing and anonymization

### Week 2: DICOM Frontend
- Day 1-2: Integrate viewer library (Cornerstone or AMI)
- Day 3-4: Build 2D and 3D viewer components
- Day 5: VR controls and testing

### Week 3: TCIA Integration
- Day 1-2: TCIA API client
- Day 3-4: Agent enhancement for imaging
- Day 5: Testing and integration

### Week 4: Imaging Search UI
- Day 1-2: Search components
- Day 3-4: Results display and preview
- Day 5: End-to-end testing and polish

**Total:** 4-5 weeks for complete implementation

---

## Competitive Analysis

### Similar Tools
1. **3D Slicer** - Desktop medical imaging viewer (open source)
2. **OHIF Viewer** - Web-based DICOM viewer (open source)
3. **Radiant DICOM Viewer** - Desktop viewer (commercial)
4. **Horos** - macOS medical viewer (open source)

### Babocument Differentiators
- **VR/XR Support:** Immersive 3D viewing
- **AI-Assisted Search:** Natural language queries
- **Integrated Workflow:** Papers + imaging in one platform
- **Research Focus:** Not clinical diagnosis, but research analysis
- **Multi-modal:** Documents, data, and images together

---

**Status:** 📝 Documented - Ready for prioritization and implementation planning

**Next Steps:**
1. Validate user interest in medical imaging feature
2. Create GitHub Issue #39
3. Prioritize relative to paper discovery features
4. Plan technical spike for DICOM viewer library selection
5. Obtain sample DICOM files from TCIA for testing

