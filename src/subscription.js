import React, { useEffect } from "react";
import { gql, useQuery, useSubscription } from "@apollo/client";
import "./subscription.css";

const SAMPLE_QUERY = gql`
  query SampleQuery {
    sample {
      result
      serverName
    }
  }
`;

const SAMPLE_SUBSCRIPTION = gql`
  subscription CountSeconds($startFrom: Int!, $upTo: Int!) {
    countSeconds(startFrom: $startFrom, upTo: $upTo) {
      time
      serverName
    }
  }
`;

function Subscription({ id }) {
  const subscription = useSubscription(SAMPLE_SUBSCRIPTION, {
    variables: { startFrom: id, upTo: 100 },
  });

  return (
    <div className="block">
      <h3>Subscription {id} </h3>
      <p>Server: {subscription.data?.countSeconds?.serverName}</p>
      <p>Result: {subscription.data?.countSeconds?.time}</p>
    </div>
  );
}

export function Queries() {
  const polling = useQuery(SAMPLE_QUERY);

  useEffect(() => {
    const timer = setTimeout(() => {
      polling.refetch();
    }, 1000);

    return () => clearTimeout(timer);
  }, [polling]);

  return (
    <div className="queries">
      <div className="block">
        <h3>Polling Query</h3>
        <p>Server: {polling.data?.sample?.serverName}</p>
        <p>Result: {polling.data?.sample?.result}</p>
      </div>
      <Subscription id="0" />
      <Subscription id="33" />
      <Subscription id="66" />
    </div>
  );
}
