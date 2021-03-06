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
import { observer } from "mobx-react-lite";
import * as React from "react";
import { useRootStore } from "../../stores";
import { ClientListHeading, ClientListTableHeading } from "./ClientList.styles";
import ClientListCard from "./ClientListCard";
import MarkedInProgressCard from "./MarkedInProgressCard";
import InProgressEmptyState from "./InProgressEmptyStateCard";

// Update this if the <ClientListHeading/> height changes
export const HEADING_HEIGHT_MAGIC_NUMBER = 118;

const ClientList = () => {
  const { clientsStore, policyStore } = useRootStore();

  let clients;
  if (clientsStore.clients) {
    clients = clientsStore.clients.map((client) => {
      const markedInProgress =
        clientsStore.clientsMarkedInProgress[client.personExternalId];

      if (markedInProgress) {
        return (
          <MarkedInProgressCard client={client} key={client.personExternalId} />
        );
      }

      return (
        <ClientListCard
          client={client}
          isInProgress={false}
          key={client.personExternalId}
        />
      );
    });
  }

  let inProgressClients;
  if (clientsStore.inProgressClients.length) {
    inProgressClients = clientsStore.inProgressClients.map((client) => {
      const markedInProgress =
        clientsStore.clientsMarkedInProgress[client.personExternalId];

      if (markedInProgress?.client.inProgressActions?.length) {
        return (
          <MarkedInProgressCard client={client} key={client.personExternalId} />
        );
      }
      return (
        <ClientListCard
          client={client}
          isInProgress
          key={client.personExternalId}
        />
      );
    });
  } else {
    inProgressClients = <InProgressEmptyState />;
  }

  return (
    <div>
      <ClientListHeading>Up Next</ClientListHeading>
      <ClientListTableHeading>
        <span>Client</span>
        <span>Needs</span>
        <span>Recommended Contact</span>
      </ClientListTableHeading>

      {clientsStore.isLoading &&
      clientsStore.clients.length === 0 &&
      policyStore.isLoading
        ? `Loading... ${clientsStore.error || ""}`
        : clients}

      <br />

      <ClientListHeading>In Progress</ClientListHeading>
      <ClientListTableHeading />
      {clientsStore.isLoading || policyStore.isLoading
        ? `Loading... ${clientsStore.error || ""}`
        : inProgressClients}
    </div>
  );
};

export default observer(ClientList);
