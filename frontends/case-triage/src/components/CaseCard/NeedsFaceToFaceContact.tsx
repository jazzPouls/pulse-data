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
import {
  Icon,
  IconSVG,
  Need,
  palette,
} from "@recidiviz/case-triage-components";
import * as React from "react";
import { Caption, CaseCardBody, CaseCardInfo } from "./CaseCard.styles";
import { DecoratedClient } from "../../stores/ClientsStore/Client";
import { useRootStore } from "../../stores";
import { SupervisionContactFrequency } from "../../stores/PolicyStore/Policy";

interface NeedsFaceToFaceContactProps {
  className: string;
  client: DecoratedClient;
}

const getLastContactedText = (client: DecoratedClient) => {
  const { mostRecentFaceToFaceDate } = client;

  if (mostRecentFaceToFaceDate) {
    return `Last contacted on ${mostRecentFaceToFaceDate.format(
      "MMMM Do, YYYY"
    )}`;
  }
  return `Assumed no contact from CIS.`;
};

const getContactFrequencyText = (
  contactFrequency?: SupervisionContactFrequency
) => {
  if (!contactFrequency) {
    return null;
  }

  const [contacts, days] = contactFrequency;
  const pluralized = contacts === 1 ? "contact" : "contacts";
  return `${contacts} ${pluralized} every ${days} days`;
};

const NeedsFaceToFaceContact: React.FC<NeedsFaceToFaceContactProps> = ({
  className,
  client,
}: NeedsFaceToFaceContactProps) => {
  const { policyStore } = useRootStore();
  const {
    needsMet: { faceToFaceContact: met },
  } = client;

  const title = met ? `Contact: Up To Date` : `Contact Needed`;
  const contactFrequency = policyStore.findContactFrequencyForClient(client);

  return (
    <CaseCardBody className={className}>
      <Need
        kind={IconSVG.NeedsContact}
        met={client.needsMet.faceToFaceContact}
      />
      <CaseCardInfo>
        <strong>{title}</strong>
        <br />
        <Caption>
          <div>
            <Icon kind={IconSVG.Place} size={10} fill={palette.text.caption} />{" "}
            {client.currentAddress || "No address on file"}
          </div>
          <div>{getContactFrequencyText(contactFrequency)}</div>
          {getLastContactedText(client)}
        </Caption>
      </CaseCardInfo>
    </CaseCardBody>
  );
};

export default NeedsFaceToFaceContact;
