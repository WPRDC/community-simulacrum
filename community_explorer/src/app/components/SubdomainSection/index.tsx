/**
 *
 * IndicatorListing
 *
 */
import React from 'react';
import {
  Divider,
  Grid,
  Heading,
  repeat,
  Text,
  View,
} from '@adobe/react-spectrum';
import { Subdomain } from '../../types';
import { Indicator } from '../../containers/Indicator';

interface Props {
  subdomain: Subdomain;
}

export function SubdomainSection({ subdomain }: Props) {
  const { name, description, indicators } = subdomain;

  return (
    <View marginBottom="size-500">
      <Heading level={4} UNSAFE_style={{ marginBottom: '4px' }}>
        {name}
      </Heading>
      <View>
        <Text>{description}</Text>
      </View>
      <Divider marginY="size-100" />
      <Grid
        columns={repeat('auto-fit', 'size-4600')}
        rows="auto"
        gap="size-250"
        marginY="size-200"
      >
        {indicators.map(indicator => (
          <View key={indicator.slug}>
            <Indicator card indicator={indicator} />
          </View>
        ))}
      </Grid>
    </View>
  );
}
