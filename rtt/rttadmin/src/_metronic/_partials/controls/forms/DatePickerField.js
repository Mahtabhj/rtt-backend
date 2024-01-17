import React from "react";
import { useField, useFormikContext } from "formik";
import DatePicker from "react-datepicker";
import dayjs from 'dayjs';

const getFieldCSSClasses = (touched, errors) => {
  const classes = ["form-control"];
  if (touched && errors) {
    classes.push("is-invalid");
  }

  if (touched && !errors) {
    classes.push("is-valid");
  }

  return classes.join(" ");
};

export function DatePickerField({ ...props }) {
  const { setFieldValue, errors, touched } = useFormikContext();
  const [field] = useField(props);

  // quick fix for RTT-297
  const convertedDate = field.value ? dayjs(field.value).format('DD/MM/YYYY') : null;

  return (
    <>
      {props.label && <label>{props.label}</label>}
      <br />
      <DatePicker
        dateFormat="dd/MM/yyyy"
        className={getFieldCSSClasses(touched[field.name], errors[field.name])}
        style={{ width: "100%" }}
        // value={convertedDate}
        showYearDropdown
        selected={(convertedDate && new Date(field.value)) || null}
        strictParsing
        onChange={(val) => {
          setFieldValue(field.name, val);
        }}
      />
      {errors[field.name] && touched[field.name] ? (
        <div className="invalid-datepicker-feedback">
          {errors[field.name].toString()}
        </div>
      ) : null}
    </>
  );
}
