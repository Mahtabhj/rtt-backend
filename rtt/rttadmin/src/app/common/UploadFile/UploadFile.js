import React from 'react';
import PropTypes from 'prop-types';
import { useDropzone } from 'react-dropzone';
// import { ProgressBar } from 'react-bootstrap';
import SVG from 'react-inlinesvg';
import cx from 'classnames';

import { formatBytes } from "@common";

import excel from './images/excel.svg';
import upload from './images/upload.svg';

import './UploadFile.scss';

const propTypes = {
  setFile: PropTypes.func.isRequired,
  file: PropTypes.object,
  progress: PropTypes.number.isRequired,
};

const defaultProps = {
  file: null,
};

export const UploadFile = ({ file, setFile, progress }) => {
  const { getRootProps, getInputProps } = useDropzone({
    accept: '.xls, .xlsx',
    multiple: false,
    onDrop: ([acceptedFile]) => {
      setFile(
        Object.assign(acceptedFile, {
          preview: URL.createObjectURL(acceptedFile),
        }),
      );
    },
  });

  return (
    <section {...getRootProps()} className={cx('upload-file', { 'upload-file--loading': file })}>
      <input {...getInputProps()} />

      {!file ? (
        <>
          <SVG src={upload} className="upload-file__logo" />
          <div className="upload-file__instruction">
            <span>Drag & Drop your file here or</span>
            <span>Browse Files</span>
          </div>
        </>
      ) : (
        <div className="upload-file__loading">
          <SVG src={excel} className="upload-file__logo" />
          <div className="upload-file__progress">
            <span>{file.name}</span>
            {/*<ProgressBar now={progress} />*/}
            <span>
              {formatBytes(file.size)}{/*&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;{progress}%*/}
            </span>
          </div>
        </div>
      )}
    </section>
  );
};

UploadFile.propTypes = propTypes;
UploadFile.defaultProps = defaultProps;
