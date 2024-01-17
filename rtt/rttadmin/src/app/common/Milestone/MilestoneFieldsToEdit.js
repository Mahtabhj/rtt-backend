import React, { useEffect, useMemo, useState } from "react";
import ReactSelect from "react-select";
import RichTextEditor from "react-rte";
import PropTypes from "prop-types";
import { ErrorMessage, Field, Form } from "formik";

import { Input, DatePickerField } from "@metronic-partials/controls";

import { SelectDocument } from "../Document/SelectDocument";
import { SelectUrl } from "../Url/SelectUrl";
import { RelatedSubstances } from "../RelatedSubstances/RelatedSubstances";

const propTypes = {
  id: PropTypes.number,
  type: PropTypes.oneOf(['regulation', 'regulatoryFramework']).isRequired,
  values: PropTypes.object.isRequired,
  setFieldValue: PropTypes.func.isRequired,
  types: PropTypes.array.isRequired,
  documents: PropTypes.array.isRequired,
  urls: PropTypes.array.isRequired,
}

const defaultProps = {
  id: null,
}

export const MilestoneFieldsToEdit = (
  {
    id,
    type,
    values,
    setFieldValue,
    types,
    documents,
    urls,
  }
) => {
  const { documents: milestoneDocuments, urls: milestoneUrls } = values;
  const [selectedDocuments, setSelectedDocuments] = useState(null);
  const [updatedDocument, setUpdatedDocument] = useState(null);

  const [selectedUrls, setSelectedUrls] = useState(null);
  const [updatedUrl, setUpdatedUrl] = useState(null);

  const handleOnChangeType = (value) => setFieldValue('type', value);
  const handleOnChangeDescription = (value) => setFieldValue('description', value);

  const substancesQueryParams = useMemo(() => (id ? { milestone_id: id } : null), [id]);

  useEffect(() => {
    if (selectedDocuments && selectedDocuments.length !== milestoneDocuments.length) {
      setFieldValue('documents', selectedDocuments);
    }
  }, [selectedDocuments, milestoneDocuments]);

  useEffect(() => {
    if (updatedDocument && selectedDocuments?.length) {
      const updatedSelectedDocuments = selectedDocuments.map(document => (
        document.id === updatedDocument.id
          ? updatedDocument
          : document
      ));

      setSelectedDocuments(updatedSelectedDocuments);
      setFieldValue('documents', updatedSelectedDocuments);
      setUpdatedDocument(null);
    }
  }, [updatedDocument, selectedDocuments]);

  useEffect(() => {
    if (selectedUrls && selectedUrls.length !== milestoneUrls.length) {
      setFieldValue('urls', selectedUrls);
    }
  }, [selectedUrls, milestoneUrls]);

  useEffect(() => {
    if (updatedUrl && selectedUrls?.length) {
      const updatedSelectedUrls = selectedUrls.map(document => (
        document.id === updatedUrl.id
          ? updatedUrl
          : document
      ));

      setSelectedUrls(updatedSelectedUrls);
      setFieldValue('urls', updatedSelectedUrls);
      setUpdatedUrl(null);
    }
  }, [updatedUrl, selectedUrls]);

  return (
    <Form className="form form-label-right">
      <div className="form-group row">
        {/* Name */}
        <div className="col-lg-6">
          <Field
            name="name"
            component={Input}
            placeholder="Name"
            label="Name *"
            withFeedbackLabel={false}
          />

          <ErrorMessage name="name">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        {/* From Date */}
        <div className="col-lg-6">
          <DatePickerField name="from_date" label="From Date *"/>
        </div>
      </div>

      <div className="form-group row">
        {/* Type */}
        <div className="col-lg-6">
          <label>Select Type</label>
          <ReactSelect
            value={values.type}
            getOptionLabel={(option) => option.title}
            getOptionValue={(option) => option.value}
            onChange={handleOnChangeType}
            name="type"
            options={types}
          />

          <ErrorMessage name="type">
            {(msg) => <div style={{ color: "red" }}>{msg}</div>}
          </ErrorMessage>
        </div>

        {/* To Date */}
        <div className="col-lg-6">
          <DatePickerField name="to_date" label="To Date *"/>
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-12">
          <SelectDocument
            type={type}
            selectedDocuments={milestoneDocuments}
            setSelectedDocuments={setSelectedDocuments}
            documentOptions={documents}
            setUpdatedDocument={setUpdatedDocument}
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-12">
          <SelectUrl
            type={type}
            selectedUrls={milestoneUrls}
            setSelectedUrls={setSelectedUrls}
            urlOptions={urls}
            setUpdatedUrl={setUpdatedUrl}
          />
        </div>
      </div>

      <div className="form-group row">
        <div className="col-lg-12">
          <RelatedSubstances queryParams={substancesQueryParams} isCard={false} />
        </div>
      </div>

      <div className="form-group row">
        {/* Description */}
        <div className="col-lg-12">
          <label>Description *</label>

          <RichTextEditor
            value={values.description}
            onChange={handleOnChangeDescription}
          />

          <ErrorMessage name="description">
            {(msg) => <div style={{ color: "#e7576c" }}>{msg}</div>}
          </ErrorMessage>
        </div>
      </div>
    </Form>
  )
}

MilestoneFieldsToEdit.propTypes = propTypes;
MilestoneFieldsToEdit.defaultProps = defaultProps;
