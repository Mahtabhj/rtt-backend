import React from "react";
import SVG from "react-inlinesvg";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

import { openExternal } from "../Images";

import './CustomLink.scss';

const propTypes = {
  id: PropTypes.number.isRequired,
  title: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['news']).isRequired,
};

export const CustomLink = ({ id, title, type }) => (
  <Link
    to={`/${type}/${id}`}
    target="_blank"
    rel="noopener noreferrer"
    className="custom-link"
  >
    {title}
    <SVG src={openExternal}/>
  </Link>
);

CustomLink.propTypes = propTypes;
