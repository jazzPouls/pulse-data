// Recidiviz - a data platform for criminal justice reform
// Copyright (C) 2021 Recidiviz, Inc.
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
// =============================================================================
import styled from "styled-components/macro";
import { rem } from "polished";
import { Button, palette } from "@recidiviz/case-triage-components";

export const InProgressOverlay = styled.div`
  display: flex;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background: ${palette.pine.main};
  align-items: center;
  padding: 0 32px;
  color: white;
  @keyframes fadeIn {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
  animation: fadeIn 0.3s;
`;

export const InProgressConfirmation = styled.div`
  margin-right: auto;
  font-size: ${rem("13px")};
`;

export const InProgressConfirmationHeading = styled.div`
  font-size: ${rem("16px")};
  font-weight: 500;
`;

export const Undo = styled(Button).attrs({ kind: "link" })`
  color: ${palette.white.main};
  font-weight: bold;

  &:active {
    color: ${palette.white.main};
  }
`;
